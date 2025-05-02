import { useState } from "react"; //way to import libraries too
import Navbar from "./components/Navbar";
import OrderInput from "./components/OrderInput";

//import component in anohter file(recommened)

//styles
import "./App.css";

//components need to start in a capital letter i think
function AnotherComponent() {
  return (
    <>
      <p>another component</p>
    </>
  );
}
// this function is a react component
function App() {
  return (
    // if you have multiple html tags, in a return statement, you need to enclose it in <div></div> or <></>
    //only html goes in the return statment
    <>
      {/* rendering another component */}
      <div className="min-h-screen transition-colors duration-500   text-gray-100">
        <div className=" flex flex-col">
          <Layout>
            <OrderInput/>
          </Layout>
        </div>
      </div>
    </>
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
  return(
    <>
      <div className="  w-4/5 h-screen mx-auto px-4">
        <Navbar />
        {children}
      </div>
    </>
  );
}
