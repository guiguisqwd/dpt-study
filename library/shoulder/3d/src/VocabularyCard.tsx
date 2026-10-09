import { useEffect, useId, useRef, useState } from 'react';
import { vocabulary, type VocabularyTerm } from './vocabulary';
import audioManifest from '../public/audio/manifest.json';
import './vocabulary-card.css';

type VocabularyCardProps = {
  term: VocabularyTerm;
  showChinese: boolean;
  onToggleChinese: () => void;
  onChoose: (id: string) => void;
};

const groups: VocabularyTerm['group'][] = ['Muscles', 'Bones', 'Landmarks', 'Acupoints'];
const groupChinese: Record<VocabularyTerm['group'], string> = {
  Muscles: '肌肉', Bones: '骨骼', Landmarks: '解剖标志', Acupoints: '穴位拼音',
};
const audioClips: Record<string, { file: string; voice: string; provider?: string }> = audioManifest.clips;

export function VocabularyCard({ term, showChinese, onToggleChinese, onChoose }: VocabularyCardProps) {
  const audioRef = useRef<HTMLAudioElement>(null);
  const requestRef = useRef(0);
  const [playing, setPlaying] = useState<'normal' | 'slow' | null>(null);
  const [error, setError] = useState('');
  const selectId = useId();
  const index = vocabulary.findIndex(item => item.id === term.id);
  const isPinyin = term.group === 'Acupoints';
  const audioClip = audioClips[term.id];
  const voiceName = audioClip?.voice === 'marin' ? 'Marin' : audioClip?.voice;
  const voiceLabel = audioClip?.provider === 'OpenAI' ? `OpenAI ${voiceName}` : voiceName;

  useEffect(() => {
    const audio = audioRef.current;
    requestRef.current += 1;
    audio?.pause();
    setPlaying(null);
    setError('');
    return () => {
      requestRef.current += 1;
      audio?.pause();
    };
  }, [term.id]);

  async function play(mode: 'normal' | 'slow') {
    const audio = audioRef.current;
    if (!audio) return;
    const request = ++requestRef.current;
    setError('');
    audio.pause();
    audio.currentTime = 0;
    audio.playbackRate = mode === 'slow' ? 0.75 : 1;
    audio.preservesPitch = true;
    try {
      await audio.play();
      if (request === requestRef.current) setPlaying(mode);
    } catch {
      if (request === requestRef.current) {
        setPlaying(null);
        setError('Audio could not play. Try again. 发音未能播放，请重试。');
      }
    }
  }

  function move(offset: number) {
    const next = vocabulary[(index + offset + vocabulary.length) % vocabulary.length];
    onChoose(next.id);
  }

  return <section className="vocab-card" aria-label="English vocabulary practice">
    <div className="vocab-topline">
      <span className="vocab-eyebrow">LEARN THE NAME</span>
      <button type="button" className="vocab-reveal" onClick={onToggleChinese} aria-pressed={showChinese}>
        {showChinese ? 'Hide Chinese' : 'Show Chinese'}
        <small>{showChinese ? '隐藏释义' : '显示释义'}</small>
      </button>
    </div>
    <div className="vocab-term-content">
      <div className="vocab-category">{term.group}{term.pointId && <span>{term.pointId}</span>}</div>
      <h2 lang={isPinyin ? 'zh-Latn' : 'en'}>{term.english}</h2>
      <div className={`vocab-meaning${showChinese ? '' : ' vocab-meaning-hidden'}`}>
        {showChinese ? <span lang="zh">{term.chinese}</span> : <span>Recall the meaning · 回想中文</span>}
      </div>
      {term.pronunciation && <p className="vocab-ipa" aria-label="Pronunciation">{term.pronunciation}</p>}
      <div className="vocab-stress">
        <span>{isPinyin ? 'Pinyin · tone marks' : 'Stress aid · CAPITALS = stress'}</span>
        <strong lang={isPinyin ? 'zh-Latn' : 'en'}>{term.stress}</strong>
      </div>
    </div>
    <div className="vocab-audio-actions">
      <button type="button" onClick={() => void play('normal')} aria-label={`Listen to ${term.english}`} aria-pressed={playing === 'normal'}>
        <span aria-hidden="true">◖))</span> Listen <small>发音</small>
      </button>
      <button type="button" onClick={() => void play('slow')} aria-label={`Slow pronunciation of ${term.english}`} aria-pressed={playing === 'slow'}>
        <span aria-hidden="true">0.75×</span> Slow <small>慢速</small>
      </button>
    </div>
    <audio ref={audioRef} src={audioClip ? `./${audioClip.file}` : undefined} preload="none" onEnded={() => setPlaying(null)} onPause={() => setPlaying(null)} aria-label={`${term.english} pronunciation`} />
    <p className="vocab-voice">{isPinyin ? 'Mandarin' : 'American English'} · {voiceLabel}<span>合成发音</span></p>
    {error && <p className="vocab-audio-error" role="alert">{error}</p>}
    <div className="vocab-word-nav">
      <label htmlFor={selectId}>Word list <span>{index + 1} / {vocabulary.length}</span></label>
      <select id={selectId} value={term.id} onChange={event => onChoose(event.target.value)}>
        {groups.map(group => <optgroup key={group} label={`${group}${showChinese ? ` · ${groupChinese[group]}` : ''}`}>
          {vocabulary.filter(item => item.group === group).map(item => <option value={item.id} key={item.id}>
            {item.english}{item.pointId ? ` · ${item.pointId}` : ''}{showChinese ? ` — ${item.chinese}` : ''}
          </option>)}
        </optgroup>)}
      </select>
      <div className="vocab-step-buttons">
        <button type="button" onClick={() => move(-1)} aria-label="Previous word">← Previous</button>
        <button type="button" onClick={() => move(1)} aria-label="Next word">Next →</button>
      </div>
    </div>
    <details className="vocab-sources">
      <summary>Pronunciation notes &amp; sources <span>读音依据</span></summary>
      <p>{isPinyin
        ? 'Acupoint names use Chinese pinyin. Tone marks and Mandarin audio help you read the original name.'
        : 'American pronunciation. CAPITALS are a stress aid, not IPA. Some IPA is converted from Merriam-Webster notation; phrase pronunciations may combine the individual words.'}</p>
      {term.pronunciationNote && <p>{term.pronunciationNote}</p>}
      <p>Audio is synthesized; dictionary links provide the pronunciation reference.</p>
      <ul>{term.sources.map((source, sourceIndex) => <li key={source}>
        <a href={source} target="_blank" rel="noreferrer">{source.includes('merriam-webster') ? 'Merriam-Webster' : source.includes('cambridge.org') ? 'Cambridge Dictionary' : 'Acupoint name reference'}{term.sources.length > 1 ? ` · ${sourceIndex + 1}` : ''} ↗</a>
      </li>)}</ul>
    </details>
  </section>;
}
