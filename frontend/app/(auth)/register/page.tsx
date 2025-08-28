'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { register } from '@/lib/api';

export default function RegisterPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await register(name, email, password);
      router.push('/login');
    } catch (e) {
      setError('Error al registrarse');
    }
  };
  return (
    <div className="flex items-center justify-center h-screen">
      <form onSubmit={submit} className="bg-white p-6 rounded shadow w-80 space-y-4">
        <h1 className="text-xl font-bold">Registro</h1>
        {error && <p className="text-red-500">{error}</p>}
        <input className="w-full border px-2 py-1" placeholder="Nombre" value={name} onChange={e => setName(e.target.value)} />
        <input className="w-full border px-2 py-1" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
        <input className="w-full border px-2 py-1" type="password" placeholder="Contraseña" value={password} onChange={e => setPassword(e.target.value)} />
        <button className="w-full bg-green-600 text-white py-2 rounded" type="submit">Registrar</button>
      </form>
    </div>
  );
}
