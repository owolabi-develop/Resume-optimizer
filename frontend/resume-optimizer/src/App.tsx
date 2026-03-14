
import HeaderSection from "./components/Header/HeaderSection"
import { CoverLetter, ResumeContainer} from "./components/ResumeContainer"
import { sampleCover,sampleResume } from "./components/samples"
import { FileText } from 'lucide-react';

function App() {

  // handle document downloads

  const handleCoverLetterDownload = () => {

  }
  const handleResumeDownload = () => {
    
  }
  const generateOptimizeResume = ()=>{

  }
  

  return (
    <>
     <section className="h-screen w-full">
      {/* headerMenu section */}
      <HeaderSection/>
      {/* headerMenu  Section */}
      
      <div className="w-full h-screen flex flex-row">
        {/* resume container */}
        <div className="w-full max-w-3/5 border-r-2 border-b-gray-600">

        <div className="headers p-2 flex flex-row justify-between">
          <div></div>
          <div className="">
            <button onClick={handleResumeDownload} className="flex items-center justify-center rounded-md gap-1 border p-1 bg-gray-800 text-white
            hover:bg-gray-800"> Download Resume<FileText size={15} color="gray"/></button>
          </div>

        </div>
        <ResumeContainer resume={sampleResume}/>

        {/* document inputs and controls */}
        <div className="w-full grid grid-cols-2 gap-2 p-2">
          <div>file</div>
           <div>
            <textarea  cols={100}id="job_description" className=" resize-none 
             border border-default-medium text-heading 
             text-sm rounded-base focus:ring-brand focus:border-brand 
             block w-full p-3.5 shadow-xs placeholder:text-body rounded-xl" 
             placeholder="Add Job Description here"></textarea>
           </div>
            <div>
               <button onClick={generateOptimizeResume} className="flex items-center justify-center rounded-md gap-1 border p-2 bg-gray-800 text-white
            hover:bg-gray-800"> Optimize Resume<FileText size={15} color="gray"/></button>
            </div>
        </div>
        {/* document inputs and controls */}
        
        
        </div>
         {/* resume container */}

           {/* chat container and coverLetter */}
          <div className="w-full max-w-2/5">
           <div className="headers p-2 flex flex-row justify-between">
          <div></div>
          <div className="">
            <button onClick={handleCoverLetterDownload} className="flex items-center justify-center rounded-md gap-1 border p-1 bg-gray-800 text-white
            hover:bg-gray-800"> Download Cover Letter<FileText size={15} color="gray"/></button>
          </div>

        </div>
           {/* coverLetter */}
           <CoverLetter coverLetter={sampleCover}/>
           {/* coverLetter */}
          </div>
           {/*  chat container and coverLetter */}

      </div>


     </section>
     
    </>
  )
}

export default App
