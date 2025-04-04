// ui/src/App.js
import React, { useState } from "react";
import { motion } from "framer-motion";
import { UploadCloud } from "lucide-react";
import "./App.css";

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [statusMsg, setStatusMsg] = useState("");

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setStatusMsg("");
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setStatusMsg("Uploading...");

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setStatusMsg(`✅ ${result.message}`);
    } catch (error) {
      setStatusMsg("❌ Upload failed.");
    }

    setUploading(false);
  };

  return (
    <div className="app">
      <motion.div
        className="upload-box"
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <UploadCloud size={48} />
        <h2>Upload Malware Sample</h2>
        <input type="file" onChange={handleFileChange} />
        <button disabled={uploading} onClick={handleUpload}>
          {uploading ? "Uploading..." : "Upload"}
        </button>
        <p>{statusMsg}</p>
      </motion.div>
    </div>
  );
}

export default App;

