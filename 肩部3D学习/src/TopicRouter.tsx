import { useEffect, useState } from 'react';
import App from './App';
import { StandardTopicViewer } from './StandardTopicViewer';
import { parseTopicCatalog, topicHref, type StudyTopic } from './topics';
import './topics.css';

const legacyShoulder: StudyTopic = {
  id: 'shoulder', title: { en: 'Shoulder', zh: '肩部' },
  summary: { en: 'Shoulder anatomy and rotator cuff', zh: '肩部解剖与肩袖' },
  status: 'published', adapter: 'shoulder',
  viewer: { enabled: true, defaultTerm: 'humerus', terms: [] },
};

function TopicNavigation({ topics, currentId }: { topics: StudyTopic[]; currentId: string }) {
  return <nav className="topic-navigation" aria-label="Study topics / 学习主题">
    <a className="platform-home" href="./study.html"><strong>Anatomy Study</strong><span>解剖学习平台</span></a>
    <label htmlFor="study-topic">Topic · 主题</label>
    <select id="study-topic" value={currentId} onChange={event => {
      const next = topics.find(topic => topic.id === event.target.value);
      if (next) location.assign(topicHref(next));
    }}>
      {!topics.some(topic => topic.id === currentId) && <option value={currentId}>Unknown topic · 未知主题</option>}
      {topics.map(topic => <option key={topic.id} value={topic.id}>{topic.title.en} · {topic.title.zh}{topic.status === 'draft' ? ' · Preview / 预览' : ''}</option>)}
    </select>
    <a className="topic-library-link" href="./study.html">All topics · 全部主题 ↗</a>
  </nav>;
}

export default function TopicRouter() {
  // Existing reading, PDF and bookmarked ?term / ?point links keep their shoulder meaning.
  const query = new URLSearchParams(location.search);
  const libraryEntry = !query.has('topic') && !query.has('term') && !query.has('point');
  const topicId = query.get('topic') ?? 'shoulder';
  const [topics, setTopics] = useState<StudyTopic[] | null>(null);
  const [error, setError] = useState('');
  useEffect(() => {
    if (libraryEntry) { location.replace('./study.html'); return; }
    const controller = new AbortController();
    fetch('./topics.json', { signal: controller.signal }).then(response => {
      if (!response.ok) throw new Error(`Topic catalog unavailable (${response.status}) / 主题目录暂不可用`);
      return response.json();
    }).then(parseTopicCatalog).then(catalog => setTopics(catalog.topics)).catch(reason => {
      if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : String(reason));
    });
    return () => controller.abort();
  }, [libraryEntry]);
  const topic = topics?.find(item => item.id === topicId);
  const preserveLegacyShoulder = topicId === 'shoulder' && !topics;
  useEffect(() => {
    const title = topic?.title || (preserveLegacyShoulder ? legacyShoulder.title : null);
    document.title = title ? `${title.en} · ${title.zh} | Anatomy Study` : 'Anatomy Study · 解剖学习平台';
  }, [topic, preserveLegacyShoulder]);

  if (libraryEntry) return <main className="topic-empty"><h1>Anatomy Study · 解剖学习平台</h1><a href="./study.html">Open topic library · 打开主题目录 →</a></main>;
  return <>
    <TopicNavigation topics={topics || [legacyShoulder]} currentId={topicId} />
    {error && <div className="topic-alert" role="status">{error}。 <button onClick={() => location.reload()}>Retry · 重试</button></div>}
    {preserveLegacyShoulder || topic?.adapter === 'shoulder' ? <App />
      : topic ? <StandardTopicViewer key={topic.id} topic={topic} />
      : <main className="topic-empty"><h1>{!topics && !error ? 'Loading topic · 正在载入主题' : 'Topic unavailable · 主题不可用'}</h1>
        <p>{!topics && !error ? 'Loading the study catalog… / 正在读取学习目录…' : `The requested topic “${topicId}” could not be opened. / 无法打开所请求的主题。`}</p>
        <a href="./study.html">Return to the topic library · 返回主题目录 →</a>
      </main>}
  </>;
}
