import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useAuth } from "./store";
import { useEffect } from "react";
import ProtectedRoute from "./components/ProtectedRoute";
import Login from "./pages/Login";
import Register from "./pages/Register";

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
              <div className="flex items-center justify-center min-h-screen">
                <h1 className="text-3xl font-bold">Сниппеты скоро появятся!</h1>
              </div>
            </ProtectedRoute>
          }
        />

        <Route path="*" element={<Navigate to="/snippets" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
