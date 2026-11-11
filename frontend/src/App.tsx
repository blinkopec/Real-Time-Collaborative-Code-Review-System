import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./store";
import { useEffect } from "react";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Snippets from "./pages/Snippets";

export default function App() {
  const loadUser = useAuth((state) => state.loadUser);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/snippets"
          element={
            <ProtectedRoute>
              <Snippets />
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/snippets" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
