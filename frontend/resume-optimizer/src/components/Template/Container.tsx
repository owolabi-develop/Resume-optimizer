

type Toggle = {
     isOpen?: boolean;
}

const TemplateContainer = ({isOpen=true}:Toggle) => {
  

  return (
    <div className={`bg-white w-xl shadow-xl absolute z-10 left-40 top-32 border border-gray-200 rounded-xl p-4 space-y-4 
    ${isOpen ? '':'hidden transition-all transition-discrete opacity-0'}`}>

      {/* Header */}
      <div className="text-sm font-semibold text-gray-700">
        Resume Template
      </div>

    
    </div>
  );
};

export default TemplateContainer;