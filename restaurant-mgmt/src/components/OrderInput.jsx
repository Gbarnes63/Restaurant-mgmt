import { PiBowlFood } from "react-icons/pi";
import { FaPlusCircle } from "react-icons/fa";

import { useState, useEffect } from "react";
import axios from "axios";

export default function OrderInput() {
  const [menuItems, setMenuItems] = useState([]);
  const [orderArray, setOrderArray] = useState([]);
  const [tableNumber, setTableNumber] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    axios
      .get("http://localhost:5001/api/menu-items")
      .then((response) => {
        setMenuItems(response.data.data);
      })
      .catch((error) => {
        console.error("Error fetching menu items:", error);
        setErrorMessage("Failed to load menu items.");
      });
  }, []);

  const submitOrder = (orderArray) => {
    if (!tableNumber) {
      setErrorMessage("Please enter a table number.");
      setSuccessMessage("");
      return;
    }

    if (orderArray.length === 0) {
      setErrorMessage("Please add items to the order.");
      setSuccessMessage("");
      return;
    }

    setErrorMessage("");
    setSuccessMessage("");

    const formattedOrder = {
      table_number: parseInt(tableNumber),
      staff_id: 2,
      menu_items: orderArray.map((item) => ({
        name: item.name,
        itemid: item.id,
        price: item.price,
        quantity: item.quantity,
      })),
    };

    console.log("Formatted Order:", formattedOrder);

    axios
      .post("http://localhost:5001/api/create_order", formattedOrder)
      .then((response) => {
        console.log("Order submitted successfully:", response.data);
        setOrderArray([]);
        setTableNumber("");
        setSuccessMessage("Order placed successfully!");
        setErrorMessage("");
      })
      .catch((error) => {
        console.error("Error submitting order:", error);
        setErrorMessage("Failed to place order. Please try again.");
        setSuccessMessage("");
      });
  };

  console.log(menuItems);

  return (
    <>
      <div className="mt-10 flex justify-center grid-cols-2 gap-3 w-full h-4/5">
        <div className="flex flex-col items-center bg-linear-to-b from-[#3B4851] to-[#737373] rounded-2xl h-full w-1/5 justify-between">
          <div className="w-4/5">
            <h1 className="mt-4 flex justify-center text-2xl">Order</h1>
            <div>
              <input
                type="number"
                id="tableNumber"
                name="tableNumber"
                value={tableNumber}
                onChange={(e) => setTableNumber(e.target.value)}
                required
                className="w-full p-2 border border-gray-600 rounded-2xl mt-3 mb-3 text-white placeholder-white "
                placeholder="Enter table number"
              />
            </div>
            {orderArray.map((item, index) => (
              <OrderItem key={index} itemData={item} />
            ))}
          </div>
          <div className="flex flex-col w-full items-center">
            {errorMessage && (
              <div className="bg-red-200 text-red-700 border border-red-700 rounded p-2 mb-2 w-4/5 text-center">
                {errorMessage}
              </div>
            )}
            {successMessage && (
              <div className="bg-green-200 text-green-700 border border-green-700 rounded p-2 mb-2 w-4/5 text-center">
                {successMessage}
              </div>
            )}
            <div className="w-4/5 font-bold mb-2">
              <div className="flex justify-between">
                <p>Total</p>
                <p>
                  £{" "}
                  {orderArray
                    .reduce(
                      (total, item) => total + item.price * item.quantity,
                      0
                    )
                    .toFixed(2)}
                </p>
              </div>
            </div>
            <button
              onClick={() => submitOrder(orderArray)}
              className="bg-[#82AA82] rounded-4xl px-4 py-2 w-4/5 mb-5 hover:translate-1 hover:bg-[#517151]"
            >
              Place order
            </button>
          </div>
        </div>

        <div className="grid grid-cols-4 grid-rows-3 gap-x-5 gap-y-6 m-5 rounded-xl w-4/5">
          {menuItems.map((item) => (
            <Tile key={item.id} item={item} setOrderArray={setOrderArray} />
          ))}
        </div>
      </div>
    </>
  );
}

function Tile({ item, setOrderArray }) {
  const { id, name, price, description } = item;

  const addItemToOrder = () => {
    setOrderArray((prevOrderArray) => {
      const existingItemIndex = prevOrderArray.findIndex(
        (existingItem) => existingItem.id === id
      );

      if (existingItemIndex !== -1) {
        const updatedOrderArray = [...prevOrderArray];
        updatedOrderArray[existingItemIndex].quantity += 1;
        return updatedOrderArray;
      } else {
        return [...prevOrderArray, { id, name, price, quantity: 1 }];
      }
    });
  };

  return (
    <div className="bg-[#85A3B7] rounded-2xl w-full flex flex-col h-full justify-between">
      <div className="flex gap-x-5 p-2">
        <PiBowlFood size={40} />
        <h1 className="font-bold">{name}</h1>
      </div>
      <div className="flex flex-col w-full justify-end items-center">
        <div className="flex justify-between w-11/12 ">
          <p>{description}</p>
        </div>
        <div className="flex justify-between w-11/12 font-bold">
          <p>Price</p>
          <p>£ {price.toFixed(2)}</p>
        </div>
        <button
          onClick={addItemToOrder}
          className="flex justify-between items-center bg-[#5B775B] rounded-4xl px-4 py-2 w-11/12 mb-3 hover:translate-y-0.5 hover:bg-[#517151]"
        >
          Add item <FaPlusCircle />
        </button>
      </div>
    </div>
  );
}

function OrderItem({ itemData }) {
  console.log(itemData.id, itemData.price, itemData.quantity);
  return (
    <>
      <div className="w-full border-2 border-red-400 flex justify-between gap-3">
        <div>
          <h1 className="font-medium">{itemData.name}</h1>
          <p className="font-medium">£ {itemData.price}</p>
        </div>
        <p className="text-sm justify-end">Units: {itemData.quantity}</p>
      </div>
    </>
  );
}