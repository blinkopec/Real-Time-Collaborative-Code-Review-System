import type { ReactNode } from "react";
import { useAuth } from "../store";
import { Navigate } from "react-router-dom";

type Props = {
  children: ReactNode;
};

export default function ProtectedRoute({ children }: Props) {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Загрузка...</div>;
  }
  if (user == null) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
