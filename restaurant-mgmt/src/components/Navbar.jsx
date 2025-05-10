import { FaUserCircle, FaSun, FaMoon } from "react-icons/fa";
import { HiHome } from "react-icons/hi";
import { useNavigate } from "react-router-dom";

export default function Navbar() {
    //used for navigating between routes i.e page
  const navigate = useNavigate();

//array of buttons of the navbar
//storing them as an array and then mapping them on allows easy addition/removal of buttons wihout affecting styling
  const navItems = [
    { label: 'Place Orders', path: '/OrderInput'},
    { label: 'View Orders', path: '/OrderkitchenView'},
    { label: 'Inventory',path: '/InventoryMGMT'},
    { label: 'Staff MGMT', path: '/StaffMGMT'},
    {label: 'Reservations', path: '/Reservations'}
  ];
//using tailwind css. Maybe tricky to read, but compared to regular css, is much quicker to implement
  return (
    
      <div className="bg-linear-to-r from-[#5B775B] to-[#A9DDA9]  rounded-2xl w-full mt-4 mx-auto px-4 ">
        <div className="flex items-center justify-between h-16">
          <h1 className="text-2xl">RESTAURANT MGMT SYSTEM</h1>
          <div className="flex-shrink-0 flex items-center">
            {/* space for potential logo */}
            {/* <img 
              src={logo} 
              alt=" Logo" 
              className="h-12 cursor-pointer hover:scale-105 transition-transform duration-300"
              onClick={() => navigate('/')}
            /> */}
          </div>

          {/* Navigation Items */}
          <div className="hidden md:flex items-center space-x-4">
            <button
                onClick={() => navigate('/')}
              className={`flex items-center px-3 py-2 rounded-xl text-sm font-medium text-white hover:bg-gray-700`}
            >
              <HiHome className="mr-1" /> Home
            </button>

                {/* mapping button array for rendering */}
            {navItems.map((item) => (
              <button
                key={item.label}
                onClick={() => navigate(item.path)}
                className={`px-3 py-2 rounded-xl text-sm font-medium text-white hover:bg-gray-700 `}
              >
                {item.label} 
              </button>
            ))}

           
          </div>

    
        </div>
      </div>
  
  );
}