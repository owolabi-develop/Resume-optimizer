import React from 'react';
import { useState,useRef} from "react"
import {Mic} from 'lucide-react';

type RecorderProps = {
  size?:string;
}





 export const Recorder: React.FC<RecorderProps> = ({size=35}) => {
   const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder>(null);
  const audioChunks = useRef<Blob[]>([])
  const streamRef = useRef<MediaStream | null>(null);
  const [audioUrl,setAudioUrl] = useState<string>()

  // show audio temporary 
 

  const startRecording = async () =>{
    try{
      // hide audio player
    const stream = await navigator.mediaDevices.getUserMedia({audio:true})
     streamRef.current = stream;
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorderRef.current = mediaRecorder
    // audio chunk
    audioChunks.current = []
    // append chunk data 
    mediaRecorder.ondataavailable = (e) =>{
      audioChunks.current.push(e.data)
    }
    mediaRecorder.onstop = () => {
    const blob = new Blob(audioChunks.current, {
      type: "audio/webm",
    });
    const url = URL.createObjectURL(blob);
    setAudioUrl(url)
    console.log("Recording finished:", blob);
  };
    // start recording
    mediaRecorder.start()
    setIsRecording(true)

} catch (err){
  console.log(`${err} permission denied`)
}
  }

  const stopRecording = () => {
    mediaRecorderRef.current?.stop()
    setIsRecording(false)
    streamRef.current?.getTracks().forEach((track) => track.stop());
    streamRef.current = null;
  
  }


  return (
    <div className={`relative`}>

   
       
        <Mic size={size} onClick={isRecording ? stopRecording : startRecording}
        className={`
          cursor-pointer text-black rounded-full p-2 transition
          hover:bg-gray-500 hover:text-white
          ${isRecording ? `bg-gray-400 animate-pulse text-white ` : ""}
        `}/>
   </div>
  );
};

