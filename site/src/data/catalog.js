export const steps = [
 {id:'s1',number:'01',name:'剧本与选题',label:'从想法到故事',description:'寻找灵感、构思角色，搭建故事与对白。',icon:'✎'},
 {id:'s2',number:'02',name:'角色与分镜',label:'让画面有迹可循',description:'设计人物、拆解镜头，规划画面叙事。',icon:'◫'},
 {id:'s3',number:'03',name:'出图',label:'创造故事画面',description:'生成场景与角色，探索画风和一致性。',icon:'◇'},
 {id:'s4',number:'04',name:'出视频',label:'让画面动起来',description:'将文字或图片转化为动态镜头。',icon:'▷'},
 {id:'s5',number:'05',name:'配音与声音',label:'为故事注入声音',description:'探索配音、语音识别与声音处理工具。',icon:'≋'},
 {id:'s6',number:'06',name:'剪辑与后期',label:'完成最后一帧',description:'剪辑、字幕、插帧与画面增强。',icon:'✂'},
];
import catalog from './projects.json';
export const projects = catalog.projects.map(p => ({...p, repo:p.full_name}));
export const capturedAt = catalog.captured_at;
export const categories = Object.fromEntries(steps.map(s=>[s.id,s]));
