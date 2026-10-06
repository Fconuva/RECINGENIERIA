/** Formato documental REC: portada, control, índice y contenido continuo. */
const fs=require('node:fs'),path=require('node:path'),sharp=require('sharp');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,ImageRun,Header,Footer,
  ExternalHyperlink,HeadingLevel,WidthType,ShadingType,PageNumber,BorderStyle,
  AlignmentType,TableOfContents,TabStopType,LeaderType,TableLayoutType}=require('docx');
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Uso: node herramientas/generar-informe-rec.cjs entrada.json salida.docx');
const data=JSON.parse(fs.readFileSync(input,'utf8').replace(/^\uFEFF/,''));
const sections=data.sections||data.pages;
const meta=data.metadata||{documentCode:'REC-COM-001',revision:'01',date:'06/10/2026',scope:'Comunidad Valenciana'};
const cover=data.cover||{label:'INFORME COMERCIAL',title:data.title,subtitle:meta.scope,
  fields:[['Documento',meta.documentCode],['Revisión',meta.revision],['Estado','Para revisión']],
  revisions:[['Rev.','Fecha','Descripción','Estado'],[meta.revision,meta.date,'Emisión para revisión','Para revisión']]};
const BLUE='1F3A5F',GRAY='6B7780',INK='17202A',WIDTH=9355;
const clean=t=>String(t).replaceAll('—','-').replaceAll('–','-');
const run=(text,o={})=>new TextRun({text:clean(text),font:'Calibri',size:21,color:INK,...o});
const p=(text,o={})=>new Paragraph({alignment:AlignmentType.JUSTIFIED,
  spacing:{after:120,line:276},widowControl:true,...o,children:[run(text,o.run||{})]});
const heading=(text,level=2,newPage=false)=>new Paragraph({
  heading:[null,HeadingLevel.HEADING_1,HeadingLevel.HEADING_2,HeadingLevel.HEADING_3][level],
  pageBreakBefore:newPage,keepNext:true,keepLines:true,
  spacing:{before:level===1?280:200,after:120},children:[run(text,{bold:true,
    size:level===1?28:level===2?23:21,color:level===3?INK:BLUE})]});
function table(rows,proportions,coverTable=false){
  const raw=proportions||Array(rows[0].length).fill(1),sum=raw.reduce((a,b)=>a+b,0);
  const widths=raw.map(v=>Math.floor(WIDTH*v/sum));widths[widths.length-1]+=WIDTH-widths.reduce((a,b)=>a+b,0);
  const border={style:BorderStyle.SINGLE,size:4,color:'B4BBC3'};
  return new Table({width:{size:WIDTH,type:WidthType.DXA},columnWidths:widths,
    layout:TableLayoutType.FIXED,rows:rows.map((row,i)=>new TableRow({tableHeader:i===0,cantSplit:true,
      children:row.map((value,j)=>new TableCell({width:{size:widths[j],type:WidthType.DXA},
        margins:{top:85,bottom:85,left:100,right:100},
        shading:{type:ShadingType.CLEAR,fill:i===0?BLUE:i%2?'EEF2F5':'FFFFFF'},
        borders:{top:border,bottom:border,left:border,right:border},
        children:[p(value,{alignment:AlignmentType.LEFT,spacing:{after:0,line:250},
          run:{size:coverTable?19:18,color:i===0?'FFFFFF':INK,bold:i===0}})]}))}))});
}
let tableCount=0,figureCount=0;
const images=new Map();
async function preload(){
  for(const s of sections)for(const b of s.blocks||[])if(b.type==='image'){
    const file=path.resolve(path.dirname(input),b.path),m=await sharp(file).metadata();
    const width=Math.min(b.width||580,600),height=width*m.height/m.width;
    images.set(b.path,{type:path.extname(file).slice(1),data:fs.readFileSync(file),
      transformation:{width,height},altText:{name:'Imagen REC',title:clean(b.caption||'Imagen conceptual'),
        description:clean(b.caption||'Imagen conceptual')}});
  }
}
function blocks(b){
  if(b.type==='h')return [heading(b.text,b.level||2)];
  if(b.type==='p')return [p(b.text)];
  if(b.type==='note')return [p(b.text,{spacing:{before:60,after:120,line:250},run:{size:19,color:GRAY}})];
  if(b.type==='link')return [new Paragraph({spacing:{after:100,line:260},children:[new ExternalHyperlink({
    link:b.url,children:[run(b.text,{size:20,color:BLUE,underline:{}})]})]})];
  if(b.type==='image')return [new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:100,after:60},
    keepNext:true,children:[new ImageRun(images.get(b.path))]}),
    p(`Figura ${++figureCount}. ${b.caption||'Imagen conceptual.'}`,{
      alignment:AlignmentType.CENTER,spacing:{after:160,line:250},run:{size:19,italics:true,color:GRAY}})];
  if(b.type==='table')return [p(`Tabla ${++tableCount}. ${b.caption||'Síntesis del apartado'}`,{
    alignment:AlignmentType.LEFT,keepNext:true,spacing:{before:100,after:80},run:{size:20,bold:true}}),
    table(b.rows,b.widths),p('',{spacing:{after:60,line:100},run:{size:4}})];
  throw Error('Bloque desconocido: '+b.type);
}
async function main(){
  await preload();
  const logo=path.resolve(__dirname,'../00_SITIO_WEB_REC/assets/rec-marca.png');
  const children=[new Paragraph({alignment:AlignmentType.RIGHT,spacing:{after:160},children:[new ImageRun({
    type:'png',data:fs.readFileSync(logo),transformation:{width:175,height:60},
    altText:{name:'Marca REC',title:'REC Ingeniería',description:'REC Ingeniería'}})]})];
  const clear={style:BorderStyle.NONE,size:0,color:BLUE};
  children.push(new Table({width:{size:WIDTH,type:WidthType.DXA},columnWidths:[WIDTH],
    rows:[new TableRow({children:[new TableCell({width:{size:WIDTH,type:WidthType.DXA},
      shading:{type:ShadingType.CLEAR,fill:BLUE},margins:{top:160,bottom:200,left:170,right:170},
      borders:{top:clear,bottom:clear,left:clear,right:clear},children:[
        p(cover.label,{alignment:AlignmentType.LEFT,spacing:{after:100,line:260},run:{size:23,bold:true,color:'FFFFFF'}}),
        p(cover.title,{alignment:AlignmentType.LEFT,spacing:{after:160,line:280},run:{size:44,bold:true,color:'FFFFFF'}}),
        p(cover.subtitle,{alignment:AlignmentType.LEFT,spacing:{after:0,line:260},run:{size:23,color:'FFFFFF'}})
      ]})]})]}));
  children.push(p('',{spacing:{after:180},run:{size:4}}),
    table([['Dato','Detalle'],...cover.fields],[2300,7055],true),
    p('CONTROL DE REVISIONES',{spacing:{before:240,after:100},run:{size:21,bold:true,color:BLUE}}),
    table(cover.revisions,[800,1600,4800,2155],true),
    p('Informe emitido para revisar el posicionamiento, los compradores y los materiales comerciales de REC Ingeniería. Las propuestas requieren validación comercial y comprobación del alcance profesional antes de su aplicación.',
      {spacing:{before:220,after:120,line:276}}),
    p('La revisión documental no sustituye la aceptación de Richard Castro Núñez ni acredita resultados de contratación.',
      {run:{size:19,color:GRAY}}),
    new Paragraph({pageBreakBefore:true,spacing:{after:200},children:[run('ÍNDICE',{size:28,bold:true,color:BLUE})]}),
    new TableOfContents('Índice',{hyperlink:true,headingStyleRange:'1-2'}),
    new Paragraph({pageBreakBefore:true,spacing:{after:0,line:20},children:[]}));
  for(const s of sections){
    children.push(heading(s.title,1,!!s.newPage));
    if(s.kicker)children.push(p(s.kicker,{run:{size:19,color:GRAY}}));
    for(const b of s.blocks)children.push(...blocks(b));
  }
  const hs=new Header({children:[new Paragraph({spacing:{after:60},
    tabStops:[{type:TabStopType.RIGHT,position:WIDTH}],children:[
      run('REC Ingeniería',{size:16,color:GRAY}),
      run('\tEstrategia comercial · '+meta.scope,{size:16,color:GRAY})]})]});
  const foot=new Footer({children:[new Paragraph({alignment:AlignmentType.RIGHT,children:[
    run(`${meta.documentCode} · Rev. ${meta.revision}  |  Página `,{size:16,color:GRAY}),
    new TextRun({font:'Calibri',size:16,color:GRAY,children:[PageNumber.CURRENT]}),
    run(' de ',{size:16,color:GRAY}),new TextRun({font:'Calibri',size:16,color:GRAY,children:[PageNumber.TOTAL_PAGES]})]})]});
  const styles={default:{document:{run:{font:'Calibri',size:21,color:INK},
      paragraph:{spacing:{after:120,line:276}}}},paragraphStyles:[
    {id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,
      run:{font:'Calibri',size:28,bold:true,color:BLUE},
      paragraph:{outlineLevel:0,keepNext:true,keepLines:true,spacing:{before:280,after:120}}},
    {id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,
      run:{font:'Calibri',size:23,bold:true,color:BLUE},
      paragraph:{outlineLevel:1,keepNext:true,keepLines:true,spacing:{before:200,after:120}}},
    {id:'Heading3',name:'Heading 3',basedOn:'Normal',next:'Normal',quickFormat:true,
      run:{font:'Calibri',size:21,bold:true,color:INK},
      paragraph:{outlineLevel:2,keepNext:true,keepLines:true}},
    ...[1,2].map(i=>({id:'TOC'+i,name:'toc '+i,basedOn:'Normal',next:'Normal',
      run:{font:'Calibri',size:i===1?21:20,color:INK},paragraph:{spacing:{after:75,line:260},
        indent:{left:i===2?260:0},tabStops:[{type:TabStopType.RIGHT,position:WIDTH,leader:LeaderType.DOT}]}}))
  ]};
  const doc=new Document({creator:'REC Ingeniería',lastModifiedBy:'REC Ingeniería',
    title:data.title,subject:'Estrategia comercial, emitida para revisión',description:'Informe de REC Ingeniería',
    styles,features:{updateFields:true},sections:[{properties:{page:{
      size:{width:11906,height:16838},margin:{top:1247,bottom:1134,left:1417,right:1134,header:720,footer:720}}},
      headers:{default:hs},footers:{default:foot},children}]});
  fs.mkdirSync(path.dirname(output),{recursive:true});
  fs.writeFileSync(output,await Packer.toBuffer(doc));
  console.log(JSON.stringify({archivo:output,formato:'REC A4',tablas:tableCount,figuras:figureCount,
    indice:'Campo TOC 1-2, requiere actualizar en Word',secciones:sections.length}));
}
main().catch(e=>{console.error(e);process.exitCode=1;});
