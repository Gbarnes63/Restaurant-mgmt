import { CiPizza } from "react-icons/ci";

import { useState,useEffect } from "react";
import axios from "axios";

export default function OrderInput() {
  const [menuItems, setMenuItems] = useState([]);

  useEffect(() => {
    axios
      .get("http://localhost:5001/api/menu-items") 
      .then((response) => {
        
        setMenuItems(response.data.data); 
      })
      .catch((error) => {
        console.error("Error fetching menu items:", error);
      });
  }, []);

  return (
    <>
      <div className="mt-10 flex justify-center grid-cols-2 gap-3 w-full h-4/5">
        <div className="flex flex-col items-center bg-linear-to-b from-[#3B4851] to-[#737373] rounded-2xl h-full w-1/5 justify-between">
          <div className="w-4/5">
            <h1 className="mt-4 flex justify-center text-2xl">Order</h1>
            <div className="w-full flex justify-between gap-3">
              <div>
                <h1 className="font-medium">Item Name</h1>
                <p className="font-medium">£ 3</p>
              </div>
              <p className="text-sm justify-end">Units: 3</p>
            </div>
          </div>
          <div className="flex flex-col w-full items-center">
            <div className="flex justify-between w-3/5 font-bold">
              <p>Total</p>
              <p>£ 3</p>
            </div>
            <button className="bg-[#82AA82] rounded-4xl px-4 py-2 w-4/5 mb-5">
              Place order
            </button>
          </div>
        </div>

        <div className="grid grid-cols-4 grid-rows-3 gap-x-5 gap-y-6 m-5 rounded-xl w-4/5">
          {menuItems.map((item) => (
            <Tile key={item.id} name={item.name} price={item.price} />
          ))}
        </div>
      </div>
    </>
  );
}

function Tile({ name, price }) {
  return (
    <div className="bg-[#85A3B7] rounded-2xl w-full flex flex-col h-full justify-between">
      <div className="flex gap-x-5 p-2">
        <CiPizza size={40} />
        <h1 className="font-bold">{name}</h1>
      </div>
      <div className="flex flex-col w-full justify-end items-center">
        <div className="flex justify-between w-11/12 font-bold">
          <p>Price</p>
          <p>£ {price.toFixed(2)}</p>
        </div>
        <button className="bg-[#5B775B] rounded-4xl px-4 py-2 w-11/12 mb-3">
          Add item+
        </button>
      </div>
    </div>
  );
}
