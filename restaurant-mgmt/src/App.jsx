import { useState } from "react"; //way to import libraries too
import Navbar from "./components/Navbar";
import OrderInput from "./components/OrderInput";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import StaffMGMT from "./components/StaffMGMT.jsx";
import LoginSection from "./components/Login.jsx";

//import component in another file(recommended)

//styles
import "./App.css";

//components need to start in a capital letter I think
function AnotherComponent() {
  return (
    <>
      <p>another component</p>
    </>
  );
}
// this function is a React component
function App() {
  return (
      // if you have multiple html tags, in a return statement, you need to enclose it in <div></div> or <></>
      //only html goes in the return statement
      <BrowserRouter>
        <>
          {/* rendering another component */}
          <div className="min-h-screen transition-colors duration-500   text-gray-100 bg-[#FFF9C4]">
            <div className=" flex flex-col">
              <Layout>
                  {/* <Routes>
                      <Route path="/" element={<OrderInput />} />
                      <Route path="/S
                      taffMGMT" element={<StaffMGMT />} />
                  </Routes> */}
                  <LoginSection/>

              </Layout>
            </div>
          </div>
        </>
      </BrowserRouter>
  );
}
export default App; //components need to have export default functionName. only once per file...use for the parent component

//can also use export default like this
//props are basically parameters

// export default function example({prop1,prop2}){
//   return(

//   )
// }

function Layout({children}) {
  return (
    <>
      <div className="  w-4/5 h-screen mx-auto px-4">
        <Navbar />
        {children}
      </div>
    </>
  );
}
