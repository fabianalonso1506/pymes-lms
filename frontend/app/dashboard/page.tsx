'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { getCourses, getModules, apiFetch, getPoints, getRanking, getRewards, redeemReward, myCertificates } from '@/lib/api';

interface Module { id: number; title: string; course_id: number; }
interface Assessment { id: number; module_id: number; }

export default function Dashboard() {
  const [modules, setModules] = useState<Module[]>([]);
  const [scores, setScores] = useState<Record<number, number>>({});
  const [rewards, setRewards] = useState<any[]>([]);
  const [points, setPoints] = useState<{points:number, medal:string}>({points:0, medal:'bronce'});
  const [ranking, setRanking] = useState<any[]>([]);
  const [certs, setCerts] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      await getCourses(); // ensures token works
      const mods: Module[] = await getModules();
      setModules(mods);
      const assessments: Assessment[] = await apiFetch('/crud/assessments');
      const sc: Record<number, number> = {};
      for (const a of assessments) {
        try {
          const attempts = await apiFetch(`/assessments/${a.id}/attempts`);
          if (attempts.length > 0) sc[a.module_id] = attempts[attempts.length - 1].score;
        } catch {}
      }
      setScores(sc);
      const pts = await getPoints();
      setPoints(pts);
      setRanking(await getRanking());
      setRewards(await getRewards());
      setCerts(await myCertificates());
    };
    load();
  }, []);

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <section>
        <h2 className="font-semibold">Módulos</h2>
        <ul className="space-y-2">
          {modules.map(m => (
            <li key={m.id} className="border p-2 flex justify-between">
              <span>{m.title}</span>
              <span>{scores[m.id] ?? 0}%</span>
              <Link className="text-blue-600" href={`/modules/${m.id}`}>Ir</Link>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="font-semibold">Mis puntos</h2>
        <p>{points.points} pts - medalla {points.medal}</p>
      </section>
      <section>
        <h2 className="font-semibold">Ranking global</h2>
        <ol className="list-decimal pl-6">
          {ranking.map((r: any, idx: number) => (
            <li key={r.user_id}>{idx + 1}. {r.name} - {r.points} pts</li>
          ))}
        </ol>
      </section>
      <section>
        <h2 className="font-semibold">Catálogo de recompensas</h2>
        <ul className="space-y-2">
          {rewards.map(r => (
            <li key={r.id} className="border p-2 flex justify-between">
              <span>{r.name} - {r.cost_points} pts</span>
              <button className="text-blue-600" onClick={async () => { await redeemReward(r.id); alert('Canje solicitado'); }}>
                Canjear
              </button>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h2 className="font-semibold">Mis certificados</h2>
        <ul className="space-y-2">
          {certs.map(c => (
            <li key={c.id} className="border p-2">
              Certificado del curso {c.course_id} - <a className="text-blue-600" href={`${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'}/certificates/${c.id}/download`} target="_blank">Descargar</a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
