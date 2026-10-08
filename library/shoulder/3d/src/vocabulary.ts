export type VocabularyTerm = {
  id: string;
  english: string;
  chinese: string;
  pronunciation?: string;
  stress: string;
  group: 'Muscles' | 'Bones' | 'Landmarks' | 'Acupoints';
  anatomy?: string;
  pointId?: string;
  sources: string[];
  pronunciationNote?: string;
};
const mw = (word: string) => `https://www.merriam-webster.com/dictionary/${encodeURIComponent(word)}`;
const medical = (word: string) => `https://www.merriam-webster.com/medical/${encodeURIComponent(word)}`;
const cambridge = (word: string) => `https://dictionary.cambridge.org/us/pronunciation/english/${word}`;
const cuff = (name: string) => `rotator-cuff-muscles-${name}-muscle`;
const bone = (name: string) => `appendicular-skeleton-${name}`;
const deltoid = (part: string) => `deltoid-muscles-${part}-part-of-deltoid-muscle`;

export const vocabulary: VocabularyTerm[] = [
  { id: 'supraspinatus', english: 'Supraspinatus', chinese: '冈上肌', stress: 'soo-pruh-spy-NAY-tuhs', group: 'Muscles', anatomy: cuff('supraspinatus'), sources: [medical('supraspinatus'), mw('supra')], pronunciationNote: '重音提示依据词典缩略标音；此项不补写完整 IPA。' },
  { id: 'infraspinatus', english: 'Infraspinatus', chinese: '冈下肌', pronunciation: '/ˌɪnfrəspaɪˈneɪtəs/', stress: 'in-fruh-spy-NAY-tuhs', group: 'Muscles', anatomy: cuff('infraspinatus'), sources: [medical('infraspinatus')] },
  { id: 'teres-minor', english: 'Teres minor', chinese: '小圆肌', pronunciation: '/ˈtɪrˌiːz ˈmaɪnər/', stress: 'TEER-eez MY-ner', group: 'Muscles', anatomy: cuff('teres-minor'), sources: [medical('pronator teres'), mw('minor')], pronunciationNote: '词组音标按 teres 与 minor 的词典读音组合。' },
  { id: 'subscapularis', english: 'Subscapularis', chinese: '肩胛下肌', pronunciation: '/ˌsʌb.skæp.jəˈler.ɪs/', stress: 'sub-skap-yuh-LAIR-iss', group: 'Muscles', anatomy: cuff('subscapularis'), sources: [cambridge('subscapularis')] },
  { id: 'rotator-cuff', english: 'Rotator cuff', chinese: '肩袖', pronunciation: '/ˈroʊ.teɪ.t̬ɚ ˌkʌf/', stress: 'ROH-tay-ter kuf', group: 'Muscles', anatomy: 'rotator-cuff-muscles', sources: ['https://dictionary.cambridge.org/us/dictionary/english/rotator-cuff'] },
  { id: 'deltoid', english: 'Deltoid', chinese: '三角肌', pronunciation: '/ˈdel.tɔɪd/', stress: 'DEL-toyd', group: 'Muscles', anatomy: 'deltoid-muscles', sources: [cambridge('deltoid')] },
  { id: 'acromial-part', english: 'Acromial part', chinese: '三角肌肩峰部', pronunciation: '/əˈkroʊ.mi.əl/ + part', stress: 'uh-KROH-mee-uhl part', group: 'Muscles', anatomy: deltoid('acromial'), sources: [cambridge('acromial')], pronunciationNote: '音标展示核心形容词 acromial；音频朗读完整词组。' },
  { id: 'clavicular-part', english: 'Clavicular part', chinese: '三角肌锁骨部', pronunciation: '/kləˈvɪk.jə.lɚ/ + part', stress: 'kluh-VIK-yuh-ler part', group: 'Muscles', anatomy: deltoid('clavicular'), sources: ['https://dictionary.cambridge.org/us/dictionary/english/clavicular'], pronunciationNote: '音标展示 clavicular；音频朗读完整词组。' },
  { id: 'spinal-part', english: 'Spinal part', chinese: '三角肌肩胛冈部', pronunciation: '/ˈspaɪ.nəl/ + part', stress: 'SPY-nuhl part', group: 'Muscles', anatomy: deltoid('scapular-spinal'), sources: [cambridge('spinal')], pronunciationNote: '此处 spinal 指肩胛冈相关部分，不译为三角肌脊柱部。' },
  { id: 'scapula', english: 'Scapula', chinese: '肩胛骨', pronunciation: '/ˈskæpjələ/', stress: 'SKAP-yuh-luh', group: 'Bones', anatomy: bone('scapula'), sources: [mw('scapula')] },
  { id: 'clavicle', english: 'Clavicle', chinese: '锁骨', pronunciation: '/ˈklævɪkəl/', stress: 'KLAV-ih-kuhl', group: 'Bones', anatomy: bone('clavicle'), sources: [mw('clavicle')] },
  { id: 'humerus', english: 'Humerus', chinese: '肱骨', pronunciation: '/ˈhjuːmərəs/', stress: 'HYOO-muh-ruhs', group: 'Bones', anatomy: bone('humerus'), sources: [cambridge('humerus')] },
  { id: 'scapular-spine', english: 'Scapular spine', chinese: '肩胛冈', pronunciation: '/ˈskæpjələr spaɪn/', stress: 'SKAP-yuh-ler SPYNE', group: 'Landmarks', anatomy: bone('scapula'), sources: [mw('scapular'), mw('spine')] },
  { id: 'inferior-angle', english: 'Inferior angle', chinese: '肩胛骨下角', pronunciation: '/ɪnˈfɪriər ˈæŋɡəl/', stress: 'in-FEER-ee-er ANG-guhl', group: 'Landmarks', anatomy: bone('scapula'), sources: [mw('inferior'), mw('angle')] },
  { id: 'acromion', english: 'Acromion', chinese: '肩峰', pronunciation: '/əˈkroʊmiən/', stress: 'uh-KROH-mee-uhn', group: 'Landmarks', anatomy: bone('scapula'), sources: [medical('acromion')] },
  { id: 'greater-tubercle', english: 'Greater tubercle', chinese: '肱骨大结节', pronunciation: '/ˈɡreɪtər ˈtuːbərkəl/', stress: 'GRAY-ter TOO-ber-kuhl', group: 'Landmarks', anatomy: bone('humerus'), sources: [mw('greater'), mw('tubercle')] },
  { id: 'infraspinous-fossa', english: 'Infraspinous fossa', chinese: '冈下窝', pronunciation: '/ˌɪnfrəˈspaɪnəs ˈfɑːsə/', stress: 'in-fruh-SPY-nuhs FAH-suh', group: 'Landmarks', anatomy: bone('scapula'), sources: [medical('infraspinous'), mw('fossa')] },
  { id: 'supraspinous-fossa', english: 'Supraspinous fossa', chinese: '冈上窝', pronunciation: '/ˌsuːprəˈspaɪnəs ˈfɑːsə/', stress: 'soo-pruh-SPY-nuhs FAH-suh', group: 'Landmarks', anatomy: bone('scapula'), sources: [cambridge('supraspinous-fossa')] },
  { id: 'posterior-shoulder', english: 'Posterior shoulder', chinese: '肩后区', pronunciation: '/pɑːˈstɪr.i.ɚ ˈʃoʊl.dɚ/', stress: 'pah-STEER-ee-er SHOHL-der', group: 'Landmarks', anatomy: cuff('teres-minor'), sources: ['https://dictionary.cambridge.org/us/dictionary/english/posterior', cambridge('shoulder')], pronunciationNote: '词组音标按 posterior 与 shoulder 的美式词典读音组合。' },
  { id: 'anterolateral-acromion', english: 'Anterolateral acromion', chinese: '肩峰前外侧', pronunciation: '/ˌæn.tə.roʊˈlæt̬.ɚ.əl əˈkroʊmiən/', stress: 'an-tuh-roh-LAT-er-uhl uh-KROH-mee-uhn', group: 'Landmarks', anatomy: bone('scapula'), sources: ['https://dictionary.cambridge.org/pronunciation/english/anterolateral', medical('acromion')], pronunciationNote: '词组音标按单词读音组合；anterolateral 采用 Cambridge 美式音标，acromion 由 Merriam-Webster 标音转写。' },
  { id: 'posterolateral-acromion', english: 'Posterolateral acromion', chinese: '肩峰后外侧', pronunciation: '/ˌpɑːs.tə.roʊˈlæt̬.ɚ.əl əˈkroʊmiən/', stress: 'pah-stuh-roh-LAT-er-uhl uh-KROH-mee-uhn', group: 'Landmarks', anatomy: bone('scapula'), sources: ['https://dictionary.cambridge.org/us/dictionary/english/posterolateral', medical('acromion')], pronunciationNote: '词组音标按单词读音组合；posterolateral 采用 Cambridge 美式音标，acromion 由 Merriam-Webster 标音转写。' },
  { id: 'posterior-deltoid', english: 'Posterior deltoid', chinese: '三角肌后部', pronunciation: '/pɑːˈstɪr.i.ɚ ˈdel.tɔɪd/', stress: 'pah-STEER-ee-er DEL-toyd', group: 'Muscles', anatomy: deltoid('scapular-spinal'), sources: ['https://dictionary.cambridge.org/us/dictionary/english/posterior', cambridge('deltoid')], pronunciationNote: '词组音标按 posterior 与 deltoid 的美式词典读音组合。' },
  ...[
    ['si11','Tianzong','天宗','tiān zōng','SI11'],
    ['si12','Bingfeng','秉风','bǐng fēng','SI12'],
    ['si9','Jianzhen','肩贞','jiān zhēn','SI9'],
    ['li15','Jianyu','肩髃','jiān yú','LI15'],
    ['te14','Jianliao','肩髎','jiān liáo','TE14'],
  ].map(([id, english, chinese, stress, pointId]) => ({ id, english, chinese, stress, pointId, group: 'Acupoints' as const, sources: ['https://www.medbox.org/index.php/dl/627a4de115110145a1723f64'], pronunciationNote: 'This is a Chinese pinyin name. Audio uses Mandarin, not English. 穴名采用汉语拼音，发音为普通话。' })),
];
export const vocabularyById = Object.fromEntries(vocabulary.map(term => [term.id, term]));
export const termForAnatomy = (anatomy: string) => vocabulary.find(term => term.anatomy === anatomy.replace(/-(right|left)$/, ''));
export const pointRelatedTerms: Record<string,string[]> = {
  SI11: ['infraspinatus','scapular-spine','inferior-angle','infraspinous-fossa'],
  SI12: ['supraspinatus','scapular-spine','supraspinous-fossa'],
  SI9: ['teres-minor','posterior-shoulder','posterior-deltoid'],
  LI15: ['deltoid','acromion','greater-tubercle','anterolateral-acromion'],
  TE14: ['posterior-deltoid','acromion','greater-tubercle','posterolateral-acromion'],
};
