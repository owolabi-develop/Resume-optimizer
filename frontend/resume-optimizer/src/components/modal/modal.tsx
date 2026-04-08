import { useState } from "react";

type Toggle = {
     isOpen?: boolean;
}

const CredentialsSettings = ({isOpen=false}:Toggle) => {
  const [apiKey, setApiKey] = useState("");
  const [model, setModel] = useState("gemini-3-flash-preview");
   const [voiceModel, setVoiceModel] = useState("gemini-3.1-flash-live-preview");

  const handleSave = () => {
    console.log({ apiKey, model });

  };

  return (
    <div className={`bg-white w-[380px] shadow-xl absolute z-10 left-10 top-25 border border-gray-200 rounded-xl p-4 space-y-4 
    ${isOpen ? '':'hidden transition-all transition-discrete opacity-0'}`}>

      {/* Header */}
      <div className="text-sm font-semibold text-gray-700">
        AI Settings
      </div>

      {/* API KEY INPUT */}
      <div className="space-y-1">
        <label className="text-xs text-gray-500">API Key</label>
        <input
          type="password"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
          placeholder="Enter your Gemini API key"
          className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
        />
      </div>

      {/* MODEL SELECT */}
      <div className="space-y-1">
        <label className="text-xs text-gray-500">Chat Model</label>
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
        >
          <option value="gemini-2.5-flash">gemini-2.5-flash</option>
          <option value="gemini-2.5-flash-lite">gemini-2.5-flash-lite</option>
          <option value="gemini-2.5-pro">gemini-2.5-pro</option>
        <option value="gemini-3.1-pro-preview">gemini-3.1-pro-preview</option>
        <option value="gemini-3-flash-preview">gemini-3-flash-preview</option>
        <option value="gemini-3.1-flash-lite-preview">gemini-3.1-flash-lite-preview</option>
        </select>

          <label className="text-xs text-gray-500">Voice Model</label>
        <select
          value={voiceModel}
          onChange={(e) => setVoiceModel(e.target.value)}
          className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black"
        >
          <option value="gemini-2.5-flash-native-audio-preview-12-2025">Gemini 2.5 Flash Live Preview</option>
          <option value="gemini-3.1-flash-live-preview">Gemini 3.1 Flash Live Preview</option>
        </select>
      </div>

      {/* SAVE BUTTON */}
      <button
        onClick={handleSave}
        className="w-full bg-black text-white py-2 rounded-lg text-sm hover:opacity-90 transition"
      >
        Save Settings
      </button>

    </div>
  );
};

export default CredentialsSettings;