'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { getModule, apiFetch, submitAttempt, awardAction } from '@/lib/api';

export default function ModulePage() {
  const params = useParams();
  const id = params?.id as string;
  const [module, setModule] = useState<any>();
  const [step, setStep] = useState(0);
  const [assessment, setAssessment] = useState<any>();
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [result, setResult] = useState<any>();

  useEffect(() => {
    const load = async () => {
      const mod = await getModule(id);
      setModule(mod);
      const assessments = await apiFetch('/crud/assessments');
      const a = assessments.find((x: any) => x.module_id === mod.id);
      setAssessment(a);
      if (a) {
        const items = await apiFetch('/crud/assessment_items');
        setQuestions(items.filter((i: any) => i.assessment_id === a.id));
      }
    };
    load();
  }, [id]);

  const submit = async () => {
    if (!assessment) return;
    const res = await submitAttempt(assessment.id, answers);
    setResult(res);
    if (res.passed) {
      await awardAction('assessment');
    }
    setStep(5);
  };

  if (!module) return <p>Cargando...</p>;

  return (
    <div className="p-6 space-y-4">
      {step === 0 && (
        <div>
          <h1 className="text-2xl font-bold">{module.title}</h1>
          <p>Introducción al módulo.</p>
          <button className="mt-4 bg-blue-600 text-white px-4 py-2" onClick={() => setStep(1)}>Comenzar</button>
        </div>
      )}
      {step === 1 && (
        <div>
          <h2 className="text-xl font-semibold">Infografía</h2>
          <p>Revisa la infografía del módulo.</p>
          <button className="mt-4 bg-blue-600 text-white px-4 py-2" onClick={() => setStep(2)}>Continuar</button>
        </div>
      )}
      {step === 2 && (
        <div>
          <h2 className="text-xl font-semibold">Micro-lecciones</h2>
          <p>Video y material descargable.</p>
          <button className="mt-4 bg-blue-600 text-white px-4 py-2" onClick={async () => { await awardAction('micro'); setStep(3); }}>Continuar</button>
        </div>
      )}
      {step === 3 && (
        <div>
          <h2 className="text-xl font-semibold">Actividad práctica</h2>
          <p>Consulta la rúbrica y realiza la actividad.</p>
          <button className="mt-4 bg-blue-600 text-white px-4 py-2" onClick={async () => { await awardAction('activity'); setStep(4); }}>Ir a evaluación</button>
        </div>
      )}
      {step === 4 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Evaluación final</h2>
          {questions.map(q => (
            <div key={q.id} className="border p-2">
              <p>{q.stem}</p>
              {JSON.parse(q.options_json).map((opt: string) => (
                <label key={opt} className="block">
                  <input type="radio" name={`q${q.id}`} value={opt} onChange={e => setAnswers({ ...answers, [q.id]: e.target.value })} /> {opt}
                </label>
              ))}
            </div>
          ))}
          <button className="bg-green-600 text-white px-4 py-2" onClick={submit}>Enviar</button>
        </div>
      )}
      {step === 5 && result && (
        <div>
          <h2 className="text-xl font-semibold">Feedback</h2>
          <p>Puntaje: {result.score}</p>
          {result.allow_retake && <p className="text-red-600">Puedes realizar un examen de recuperación.</p>}
        </div>
      )}
    </div>
  );
}
