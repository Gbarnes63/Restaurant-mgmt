import { FaUserCircle, FaSun, FaMoon } from "react-icons/fa";
import { HiHome } from "react-icons/hi";

// import { useNavigate } from "react-router-dom";

export default function Navbar() {
//   const navigate = useNavigate();

  const navItems = [
    { label: 'Orders',  },
    { label: 'Inventory',},
    { label: 'Staff MGMT' }
  ];

  return (
    <nav className={` sticky top-0 z-50  text-black'} `}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          <div className="flex-shrink-0 flex items-center">
            {/* <img 
              src={logo} 
              alt="PRS Logo" 
              className="h-12 cursor-pointer hover:scale-105 transition-transform duration-300"
              onClick={() => navigate('/')}
            /> */}
          </div>

          {/* Navigation Items */}
          <div className="hidden md:flex items-center space-x-4">
            <button 
            //   onClick={() => navigate('/')}
              className={`flex items-center px-3 py-2 rounded-xl text-sm font-medium text-blue-300 hover:bg-gray-700`}
            >
              <HiHome className="mr-1" /> Home
            </button>

            {navItems.map((item) => (
              <button
                key={item.label}
                // onClick={() => navigate(`/login/${item.type}`)}
                className={`px-3 py-2 rounded-xl text-sm font-medium text-blue-300 hover:bg-gray-700 `}
              >
                {item.label} 
              </button>
            ))}

            <button
            //   onClick={() => navigate('/dashboard')}
              className={`px-3 py-2 rounded-md text-sm font-medium text-blue-300 hover:bg-gray-700`}
            >
              Dashboard
            </button>

           

            <div className="ml-4 flex items-center md:ml-6">
              <button className="flex items-center space-x-2">
                <FaUserCircle size={24} className='text-blue-300' />
              </button>
            </div>
          </div>

          {/* Mobile menu button */}
    
        </div>
      </div>
    </nav>
  );
}