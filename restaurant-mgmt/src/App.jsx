import { useState } from "react"; //way to import libraries too
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Reservations from "./components/Reservations";
import Navbar from "./components/Navbar";
import OrderInput from "./components/OrderInput";
import StaffMGMT from "./components/StaffMGMT";
import InventoryMGMT from "./components/InventoryMGMT";
import LoginSection from "./components/Login";
import OrderKitchenView from "./components/OrderKitchenView";
import ProtectedRoute from "./components/ProtectedRoute";

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
    <BrowserRouter>
      <>
        <div className="min-h-screen transition-colors duration-500 text-gray-100">
          <div className="flex flex-col">
            <Routes>
              <Route path="/login" element={<LoginSection />} />
              <Route
                path="/*"
                element={
                  <Layout>
                    <Routes>
                      <Route
                        path="/"
                        element={
                          <ProtectedRoute>
                            <Home />
                          </ProtectedRoute>
                        }
                      />
                      <Route
                        path="/StaffMGMT"
                        element={
                          <ProtectedRoute>
                            <StaffMGMT />
                          </ProtectedRoute>
                        }
                      />
                      <Route
                        path="/OrderInput"
                        element={
                          <ProtectedRoute>
                            <OrderInput />
                          </ProtectedRoute>
                        }
                      />
                      <Route
                        path="/Reservations"
                        element={
                          <ProtectedRoute>
                            <Reservations />
                          </ProtectedRoute>
                        }
                      />
                      <Route
                        path="/InventoryMGMT"
                        element={
                          <ProtectedRoute>
                            <InventoryMGMT />
                          </ProtectedRoute>
                        }
                      />
                      <Route
                        path="/OrderKitchenView"
                        element={
                          <ProtectedRoute>
                            <OrderKitchenView />
                          </ProtectedRoute>
                        }
                      />
                    </Routes>
                  </Layout>
                }
              />
            </Routes>
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

function Layout({ children }) {
  return (
    <>
      <div className="  w-4/5 h-screen mx-auto px-4">
        <Navbar />
        {children}
      </div>
    </>
  );
}
