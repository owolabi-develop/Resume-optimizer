import { Menu } from 'lucide-react';

const HeaderSection = () => {
  return (
    <div className="w-full bg-mist-800 p-4 text-amber-50 flex flex-row gap-8">
        <div className="config-menu flex items-center justify-center"><Menu 
        size={30} className='hover:text-blue-400 cursor-pointer'/>
        </div>
        <div className="flex items-center justify-center">
            <h1 className='font-semibold'>Resume Optimizer</h1>
        </div>

    </div>
  )
}

export default HeaderSection