'use client';
import { useState, useEffect } from 'react';
import { postDnc, issueCertificate, pendingRedemptions, updateRedemption } from '@/lib/api';

export default function AdminPage() {
  const [positionId, setPositionId] = useState(1);
  const [result, setResult] = useState<any>();
  const [userId, setUserId] = useState(1);
  const [courseId, setCourseId] = useState<number>();
  const [pendings, setPendings] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      setPendings(await pendingRedemptions());
    };
    load();
  }, []);

  const runDnc = async () => {
    const res = await postDnc(positionId, {});
    setResult(res);
  };

  const emit = async () => {
    if (courseId) {
      await issueCertificate(userId, courseId);
      alert('Constancia emitida');
    }
  };

  const handleRedemption = async (id: number, status: string) => {
    await updateRedemption(id, status);
    setPendings(await pendingRedemptions());
  };

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Panel RRHH</h1>
      <section className="space-y-2">
        <h2 className="font-semibold">DNC</h2>
        <label className="block">Puesto ID
          <input className="border p-1 ml-2" type="number" value={positionId} onChange={e => setPositionId(parseInt(e.target.value))} />
        </label>
        <button className="bg-blue-600 text-white px-4 py-2" onClick={runDnc}>Procesar</button>
        {result && (
          <div className="mt-2">
            <pre className="bg-gray-100 p-2">{JSON.stringify(result.gaps, null, 2)}</pre>
            <p>Obligatorios: {result.mandatory_courses.join(', ')}</p>
            <p>Optativos: {result.optional_courses.join(', ')}</p>
          </div>
        )}
      </section>
      <section className="space-y-2">
        <h2 className="font-semibold">Emitir constancia interna</h2>
        <label className="block">User ID
          <input className="border p-1 ml-2" type="number" value={userId} onChange={e => setUserId(parseInt(e.target.value))} />
        </label>
        <label className="block">Curso ID
          <input className="border p-1 ml-2" type="number" value={courseId ?? ''} onChange={e => setCourseId(parseInt(e.target.value))} />
        </label>
        <button className="bg-green-600 text-white px-4 py-2" onClick={emit}>Emitir</button>
      </section>
      <section className="space-y-2">
        <h2 className="font-semibold">Aprobar canjes</h2>
        <ul className="space-y-2">
          {pendings.map(p => (
            <li key={p.id} className="border p-2 flex justify-between">
              <span>Redención {p.id} - reward {p.reward_id}</span>
              <div className="space-x-2">
                <button className="text-green-600" onClick={() => handleRedemption(p.id, 'approved')}>Aprobar</button>
                <button className="text-red-600" onClick={() => handleRedemption(p.id, 'rejected')}>Rechazar</button>
              </div>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
