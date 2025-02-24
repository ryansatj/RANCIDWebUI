import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import './index.css'
import ConfigDetailPage from './ConfigDetailsPage.jsx';
import LogsPage from './LogsPage.jsx';
import LogDetailsPage from './LogDetailsPage.jsx';
import RouterLogs from './RouterLogs.jsx';
import RouterLogsDetails from './RouterLogsDetails.jsx';

// Create a root element
const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
  },
  {
    path: "/config/:configName",
    element: <ConfigDetailPage/>,
  },
  {
    path: "/logs",
    element: <LogsPage/>,
  },
  {
    path: "/log/:logName",
    element: <LogDetailsPage/>,
  },
  {
    path: "/rlogs",
    element: <RouterLogs/>,
  },
  {
    path: "/rlogs/:logname",
    element: <RouterLogsDetails/>,
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

