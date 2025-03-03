document.addEventListener("DOMContentLoaded", function () {
  // Elements
  const scenarioOptions = document.querySelectorAll(".scenario-option");
  const emailInput = document.querySelector(".email-input");
  const startButton = document.getElementById("start-assistant");
  const voiceInterface = document.querySelector(".voice-interface");
  const micButton = document.querySelector(".mic-button");
  const statusDisplay = document.querySelector(".status");
  const conversationSection = document.querySelector(".conversation");
  const messagesContainer = document.getElementById("messages-container");
  const userEmailInput = document.getElementById("user-email");

  // State variables
  let selectedScenario = null;
  let needsEmail = false;
  let isRecording = false;
  let mediaRecorder = null;
  let audioChunks = [];
  let socket = null;
  let audioQueue = [];
  let isPlaying = false;

  // Audio context for playing response
  let audioContext = null;

  // Select scenario
  scenarioOptions.forEach((option) => {
    option.addEventListener("click", function () {
      // Remove active class from all options
      scenarioOptions.forEach((opt) => opt.classList.remove("active"));

      // Add active class to clicked option
      this.classList.add("active");

      // Update selected scenario
      selectedScenario = this.getAttribute("data-scenario");
      needsEmail = this.getAttribute("data-needs-email") === "true";

      // Show/hide email input based on scenario
      if (needsEmail) {
        emailInput.style.display = "block";
      } else {
        emailInput.style.display = "none";
      }

      // Enable start button
      validateStartButton();
    });
  });

  // Validate email and enable/disable start button
  userEmailInput.addEventListener("input", validateStartButton);

  function validateStartButton() {
    if (!selectedScenario) {
      startButton.disabled = true;
      return;
    }

    if (needsEmail && !userEmailInput.value) {
      startButton.disabled = true;
      return;
    }

    startButton.disabled = false;
  }

  // Start assistant
  startButton.addEventListener("click", function () {
    // Hide scenario selector
    document.querySelector(".scenario-selector").style.display = "none";

    // Show voice interface and conversation
    voiceInterface.style.display = "block";
    conversationSection.style.display = "block";

    //get the current scenario and email
    const email = userEmailInput.value;

    // Initialize WebSocket connection
    initializeWebSocket(selectedScenario, email);

    // Initialize audio context
    try {
      window.AudioContext = window.AudioContext || window.webkitAudioContext;
      audioContext = new AudioContext();
    } catch (e) {
      statusDisplay.textContent =
        "Web Audio API is not supported in this browser";
    }
  });

  // Initialize WebSocket connection
  async function initializeWebSocket(scenario, email) {
    //send post request to update the handler

    statusDisplay.textContent = "Please Wait...";
    await fetch(`${window.location.href}update`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        scenario,
        email,
      }),
    });

    const wsUrl = `ws://${window.location.host}/ws`;

    socket = new WebSocket(wsUrl);

    socket.onopen = function () {
      statusDisplay.textContent = "Connected to assistant";
    };

    socket.onmessage = function (event) {
      // Check if binary data (audio chunk)
      if (event.data instanceof Blob) {
        // Add to audio queue
        audioQueue.push(event.data);

        // Start playing if not already playing
        if (!isPlaying) {
          playNextAudio();
        }
      } else {
        const data = JSON.parse(event.data);
        console.log("DATA",data);
        addMessage(data.text, data.speaker);
      }
    };

    socket.onclose = function () {
      statusDisplay.textContent = "Disconnected from assistant";
    };

    socket.onerror = function (error) {
      statusDisplay.textContent = "Connection error";
      console.error("WebSocket error:", error);
    };
  }

  // Microphone button
  micButton.addEventListener("click", function () {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  });

  // Start recording
  async function startRecording() {
    if (isRecording) return;
    console.log("STARTED RECORDING");

    // Clear audioChunks array to ensure we start fresh
    audioChunks = [];
    isRecording = true;

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      // Visual feedback
      micButton.classList.add("recording");
      statusDisplay.textContent = "Recording...";

      mediaRecorder = new MediaRecorder(stream);

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        console.log("Audio stopped, chunks:", audioChunks.length);

        if (audioChunks.length > 0) {
          const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          const mp3Blob = await convertToMp3WithLamejs(audioBlob);

          try {
            // Send audio data to server if socket is connected
            if (socket && socket.readyState === WebSocket.OPEN) {
              // Send as binary data
              console.log(mp3Blob);
              socket.send(mp3Blob);
              console.log("Audio data sent to server");
            } else {
              console.error("WebSocket not connected");
              statusDisplay.textContent = "Connection error. Please refresh.";
            }
          } catch (error) {
            console.error("Error sending audio:", error);
            statusDisplay.textContent = "Error sending audio";
          }
        } else {
          console.warn("No audio data captured");
          statusDisplay.textContent = "No audio captured. Try again.";
        }

        // Release microphone
        stream.getTracks().forEach((track) => track.stop());
      };

      // Start recording with 10ms time slices
      mediaRecorder.start(10);
    } catch (error) {
      console.error("Error accessing microphone:", error);
      statusDisplay.textContent = "Microphone access error";
      isRecording = false;
    }
  }

  // Stop recording
  function stopRecording() {
    console.log("Stopping recording");
    if (!isRecording) return;

    statusDisplay.textContent = "Processing...";
    micButton.classList.remove("recording");
    isRecording = false;

    if (mediaRecorder && mediaRecorder.state !== "inactive") {
      mediaRecorder.stop();
    }
  }

  async function convertToMp3WithLamejs(audioBlob) {
    // Convert blob to array buffer
    const arrayBuffer = await audioBlob.arrayBuffer();

    // Create audio context
    const audioContext = new (window.AudioContext ||
      window.webkitAudioContext)();

    // Decode the audio data
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer);

    // Get the PCM data from the left channel (mono conversion for simplicity)
    const samples = audioBuffer.getChannelData(0);

    // MP3 encoder configuration
    const sampleRate = audioBuffer.sampleRate;
    const bitRate = 128; // 128kbps

    // Create MP3 encoder
    const mp3encoder = new lamejs.Mp3Encoder(1, sampleRate, bitRate);

    // Process the PCM data in chunks
    const chunkSize = 1152; // Must be multiple of 576 for lamejs
    const mp3Data = [];

    // Convert float samples to int16 samples
    const int16Samples = new Int16Array(samples.length);
    for (let i = 0; i < samples.length; i++) {
      // Convert from -1.0...1.0 to -32768...32767
      int16Samples[i] =
        samples[i] < 0
          ? Math.max(-32768, Math.floor(samples[i] * 32768))
          : Math.min(32767, Math.floor(samples[i] * 32767));
    }

    // Process in chunks
    for (let i = 0; i < int16Samples.length; i += chunkSize) {
      const chunk = int16Samples.subarray(i, i + chunkSize);
      const mp3buf = mp3encoder.encodeBuffer(chunk);
      if (mp3buf.length > 0) {
        mp3Data.push(mp3buf);
      }
    }

    // Finalize encoding
    const mp3buf = mp3encoder.flush();
    if (mp3buf.length > 0) {
      mp3Data.push(mp3buf);
    }

    // Create blob from MP3 data
    return new Blob(mp3Data, { type: "audio/mp3" });
  }

  // Play next audio in queue
  function playNextAudio() {
    if (audioQueue.length === 0) {
      isPlaying = false;
      return;
    }

    isPlaying = true;
    const audioBlob = audioQueue.shift();

    const audioUrl = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioUrl);

    audio.onended = function () {
      URL.revokeObjectURL(audioUrl);
      playNextAudio();
    };

    audio.play().catch((error) => {
      console.error("Error playing audio:", error);
      playNextAudio();
    });
  }

  // Add message to conversation
  function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(
      sender === "user" ? "user-message" : "bot-message"
    );

    messageDiv.textContent = text;

    // Add speaker icon for bot messages
    if (sender === "bot") {
      const speakerIcon = document.createElement("i");
      speakerIcon.classList.add("fas", "fa-volume-up", "speaker-icon");
      speakerIcon.addEventListener("click", function () {
        // Text-to-speech for replaying the message
        if ("speechSynthesis" in window) {
          const utterance = new SpeechSynthesisUtterance(text);
          utterance.lang = "hi-IN"; // Hindi language
          speechSynthesis.speak(utterance);
        }
      });
      messageDiv.appendChild(speakerIcon);
    }

    messagesContainer.appendChild(messageDiv);

    // Scroll to bottom
    conversationSection.scrollTop = conversationSection.scrollHeight;
  }
});
