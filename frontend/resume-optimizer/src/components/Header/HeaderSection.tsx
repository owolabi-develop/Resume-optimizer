import { Menu,X } from 'lucide-react';
import CredentialsSettings from '../modal/modal';
import { useState } from 'react';


const HeaderSection = () => {
  const [openSetting, setOpenSettings] = useState(false)
  return (
    <div>
      <CredentialsSettings isOpen={openSetting}/>
    <div className="w-full bg-mist-800 p-4 text-amber-50 flex flex-row gap-8">
        <div className="config-menu flex items-center justify-center">
          {openSetting ? ( <X size={30}  onClick={() => setOpenSettings(false)}/>):
          ( <Menu size={30} className='hover:text-blue-400 cursor-pointer' onClick={() => setOpenSettings(true)}/>)}
         
        </div>
        <div className="flex items-center justify-center">
            <h1 className='font-semibold'>Resume Optimizer</h1>
        </div>

    </div>
    </div>
  )
}

export default HeaderSection