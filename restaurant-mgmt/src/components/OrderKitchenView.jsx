import React from 'react';

const mockOrders = [
  {
    orderId: 'ORD001',
    tableNumber: 5,
    orderTime: '2025-05-08 22:10',
    items: [
      { name: 'Burger', quantity: 1 },
      { name: 'Fries', quantity: 1 },
      { name: 'Coke', quantity: 1 },
    ],
    status: 'Pending',
  },
  {
    orderId: 'ORD002',
    tableNumber: 2,
    orderTime: '2025-05-08 22:12',
    items: [
      { name: 'Pizza', quantity: 1 },
      { name: 'Salad', quantity: 1 },
      { name: 'Water', quantity: 2 },
    ],
    status: 'Processing',
  },
  {
    orderId: 'ORD003',
    tableNumber: 8,
    orderTime: '2025-05-08 22:15',
    items: [
      { name: 'Pasta', quantity: 2 },
      { name: 'Garlic Bread', quantity: 1 },
      { name: 'Lemonade', quantity: 2 },
    ],
    status: 'Ready',
  },
  {
    orderId: 'ORD004',
    tableNumber: 1,
    orderTime: '2025-05-08 22:18',
    items: [
      { name: 'Steak', quantity: 1 },
      { name: 'Potatoes', quantity: 1 },
      { name: 'Red Wine', quantity: 1 },
    ],
    status: 'Served',
  },
];

function handleStatusUpdate(orderId, newStatus) {
  console.log(`Order ${orderId} status updated to: ${newStatus}`);
  //implement api fetch here
}

function OrderKitchenView() {
  return (
    <div className="w-4/5 h-screen mx-auto px-4 mt-10">
      <h1 className="text-3xl font-bold mb-6 text-black">Order Kitchen View</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {mockOrders.map((order) => (
          <div
            key={order.orderId}
            className="bg-linear-to-b from-[#5B775B] to-[#A9DDA9]  rounded-2xl p-6 flex flex-col justify-between shadow-md"
          >
            <div>
              <h2 className="text-xl font-semibold mb-2">Order: {order.orderId}</h2>
              <p className="text-gray-700 mb-1">Table: {order.tableNumber}</p>
              <p className="text-gray-700 mb-2">Time: {order.orderTime}</p>
              <h3 className="font-semibold mb-1">Items:</h3>
              <ul className="list-disc list-inside text-gray-700">
                {order.items.map((item, index) => (
                  <li key={index}>
                    {item.quantity} x {item.name}
                  </li>
                ))}
              </ul>
            </div>
            <div className="mt-4">
              <p className="font-semibold mb-2">
                Status: <span className={
                  order.status === 'Pending' ? 'text-yellow-500' :
                  order.status === 'Processing' ? 'text-blue-500' :
                  order.status === 'Ready' ? 'text-green-500' :
                  'text-gray-500'
                }>{order.status}</span>
              </p>
              <div className="flex gap-2">
                {order.status === 'Pending' && (
                  <button
                    onClick={() => handleStatusUpdate(order.orderId, 'Processing')}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded text-sm"
                  >
                    Process
                  </button>
                )}
                {order.status === 'Processing' && (
                  <button
                    onClick={() => handleStatusUpdate(order.orderId, 'Ready')}
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded text-sm"
                  >
                    Ready
                  </button>
                )}
                {order.status === 'Ready' && (
                  <button
                    onClick={() => handleStatusUpdate(order.orderId, 'Served')}
                    className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded text-sm"
                  >
                    Served
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default OrderKitchenView;