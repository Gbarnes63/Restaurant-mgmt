import { useState } from 'react'//way to import libraries too
import Navbar from './components/Navbar'

//import component in anohter file(recommened)

//styles
import './App.css'

//components need to start in a capital letter i think
function AnotherComponent (){
  return(
    <> 
      <p>another component</p>
    </>
  )
}
// this function is a react component
function App() {
  
  return (
    // if you have multiple html tags, in a return statement, you need to enclose it in <div></div> or <></>
    //only html goes in the return statment
    <> 
  {/* rendering another component */}
    <div className='min-h-screen transition-colors duration-500  bg-gradient-to-br from-gray-800 via-gray-750 to-yellow-200 text-gray-100'>
   <Navbar/>
    <h1 className='to be use if we decide to use tailwindcss for styling(i recommend it)'>Restaurant MGMT says hi</h1>
    </div>
    </>
  )
}
export default App //components need to have export default functionName. only once per file...use for the parent component

//can also use export default like this
//props are basically parameters

// export default function example({prop1,prop2}){
//   return(

//   )
// }
