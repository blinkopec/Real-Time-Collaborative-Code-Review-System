import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../store";
import { useActionState } from "react";
import { login } from "../api";

export default function Login() {
  const navigate = useNavigate();
  const loadUser = useAuth((state) => state.loadUser);

  const [error, formAction, isPending] = useActionState(loginAction, null);

  async function loginAction(prevState: any, formData: FormData) {
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;
    try {
      await login(email, password);
      await loadUser();
      navigate("/snippets");
      return null;
    } catch {
      return "Неверная почта или пароль";
    }
  }
  return (
    <form
      action={formAction}
      className="flex flex-col gap-4 max-w-sm mx-auto mt-20 p-6 bg-slate-800 rounded-lg"
    >
      <div className="w-full max-w-sm space-y-4 rounded-xl bg-slate-800 p-8 shadow-lg">
        <h1 className="text-2xl font-semibold text-white text-center">Вход</h1>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <input
          name="email"
          required
          type="email"
          className="w-full rounded-lg bg-slate-700 px-3 py-2 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Введите email"
        ></input>
        <input
          name="password"
          required
          type="password"
          className="w-full rounded-lg bg-slate-700 px-3 py-2 text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Введите пароль"
        ></input>
        <button
          type="submit"
          disabled={isPending}
          className="w-full rounded-lg bg-indigo-600 py-2 font-medium text-white hover:bg-indigo-500 disabled:opacity-50"
        >
          {isPending ? "Вход..." : "Войти"}
        </button>
        <Link
          to="/register"
          className="text-indigo-400 hover:underline text-sm block text-center"
        >
          Нет аккаунта? Зарегистрируйтесь
        </Link>
      </div>
    </form>
  );
}
