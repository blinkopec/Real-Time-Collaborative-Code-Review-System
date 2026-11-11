import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "../store";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { createSnippet, fetchSnippets } from "../api";

export default function Snippets() {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const logout = useAuth((state) => state.logout);
  const queryClient = useQueryClient();
  const { data: snippets = [], isLoading } = useQuery({
    queryKey: ["snippets"],
    queryFn: fetchSnippets,
  });

  const createMutation = useMutation({
    mutationFn: createSnippet,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["snippets"] });
      setIsFormOpen(false);
    },
  });

  async function handleAction(formData: FormData) {
    const title = formData.get("title") as string;
    const language = formData.get("language") as string;
    const code = formData.get("code") as string;

    createMutation.mutate({ title, language, code });
  }
  return (
    <div className="mx-auto max-w-4xl space-y-6 p-6">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-white">Мои сниппеты</h1>
        <button
          onClick={logout}
          className="rounded bg-slate-700 px-3 py-1 text-sm hover:bg-slate-600"
        >
          Выйти
        </button>
      </header>
      <button
        onClick={() => setIsFormOpen(!isFormOpen)}
        className="rounded bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-500"
      >
        {isFormOpen ? "Скрыть форму" : "Создать сниппет"}
      </button>
      {isFormOpen && (
        <form
          action={handleAction}
          className="space-y-2 rounded-2xl bg-slate-800 p-4"
        >
          <input
            name="title"
            placeholder="Название"
            className="w-full rounded bg-slate-700 px-3 py-2 text-white"
          />
          <select
            name="language"
            className="w-full rounded bg-slate-700 px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
            <option value="typescript">TypeScript</option>
            <option value="sql">SQL</option>
          </select>
          <textarea
            name="code"
            placeholder="Код..."
            className="h-40 w-full rounded bg-slate-700 px-3 py-2 font-mono text-sm text-white"
          />
          <button
            type="submit"
            className="rounded bg-indigo-500 px-4 py-2 font-medium text-white hover:bg-indigo-400"
            disabled={createMutation.isPending}
          >
            {createMutation.isPending ? "Создаем" : "Создать"}
          </button>
        </form>
      )}

      {isLoading ? (
        <div className="text-slate-400">Загрузка...</div>
      ) : (
        <ul className="space-y-2">
          {snippets.map((s) => (
            <li className="rounded-2xl bg-slate-800 p-4">
              <Link
                to={`/rooms/${s.id}`}
                className="text-lg font-medium text-indigo-400 hover:underline"
              >
                {s.title}
              </Link>
              <div className="text-xs text-slate-400">{s.language}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
