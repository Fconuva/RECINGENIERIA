const fs=require('node:fs');
const path=require('node:path');
const {Document,Packer,Paragraph,TextRun,Table,TableRow,TableCell,ImageRun,Header,Footer,ExternalHyperlink,HeadingLevel,WidthType,ShadingType,PageNumber,BorderStyle}=require('docx');
const [input,output]=process.argv.slice(2);
if(!input||!output)throw Error('Uso: node herramientas/generar-informe.cjs entrada.json salida.docx');
const data=JSON.parse(fs.readFileSync(input,'utf8').replace(/^\uFEFF/,''));
const ink='18344B',blue='123A62',muted='526574',width=9750;
const p=(text,options={})=>new Paragraph({spacing:{after:130,line:285},...options,children:[new TextRun({text,size:21,color:ink,...(options.run||{})})]});
const heading=(text)=>new Paragraph({heading:HeadingLevel.HEADING_2,spacing:{before:150,after:100},children:[new TextRun({text,bold:true,color:blue,size:25})]});
function block(b){
 if(b.type==='h')return heading(b.text);
 if(b.type==='p')return p(b.text);
 if(b.type==='note')return p(b.text,{spacing:{before:110,after:120,line:250},run:{size:18,color:muted}});
 if(b.type==='image')return new Paragraph({spacing:{after:150},children:[new ImageRun({type:path.extname(b.path).slice(1),data:fs.readFileSync(path.resolve(path.dirname(input),b.path)),transformation:{width:b.width||650,height:b.height||210},altText:{name:'Visual REC',title:b.caption||'Imagen conceptual',description:b.caption||'Imagen conceptual de ingeniería'}})]});
 if(b.type==='link')return new Paragraph({spacing:{after:95,line:250},children:[new ExternalHyperlink({link:b.url,children:[new TextRun({text:b.text,color:blue,underline:{},size:19})]})]});
 if(b.type==='table'){
  const widths=b.widths||Array(b.rows[0].length).fill(Math.floor(width/b.rows[0].length)); widths[widths.length-1]+=width-widths.reduce((a,c)=>a+c,0);
  return new Table({width:{size:width,type:WidthType.DXA},columnWidths:widths,rows:b.rows.map((row,i)=>new TableRow({tableHeader:i===0,cantSplit:true,children:row.map((text,j)=>new TableCell({width:{size:widths[j],type:WidthType.DXA},margins:{top:100,bottom:100,left:130,right:130},shading:{type:ShadingType.CLEAR,fill:i===0?blue:i%2?'F3F6F8':'FFFFFF'},borders:{top:{style:BorderStyle.SINGLE,size:2,color:'D8E1E6'},bottom:{style:BorderStyle.SINGLE,size:2,color:'D8E1E6'},left:{style:BorderStyle.SINGLE,size:2,color:'D8E1E6'},right:{style:BorderStyle.SINGLE,size:2,color:'D8E1E6'}},children:[p(text,{spacing:{after:0,line:235},run:{size:18,color:i===0?'FFFFFF':ink,bold:i===0}})]}))}))});
 }
 throw Error('Bloque desconocido: '+b.type);
}
const children=[];
data.pages.forEach((page,i)=>{
 children.push(new Paragraph({heading:HeadingLevel.HEADING_1,pageBreakBefore:i>0,spacing:{after:190},children:[new TextRun({text:page.title,bold:true,color:ink,size:i===0?46:34})]}));
 if(page.kicker)children.push(p(page.kicker,{run:{size:18,color:muted}}));
 page.blocks.forEach(b=>children.push(block(b)));
});
const doc=new Document({creator:'REC Ingeniería',lastModifiedBy:'REC Ingeniería',title:data.title,subject:'Propuesta comercial para revisión',description:'Análisis y materiales de REC Ingeniería',styles:{default:{document:{run:{font:'Arial',size:21,color:ink}}},paragraphStyles:[{id:'Heading1',name:'Heading 1',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:'Arial',size:34,bold:true,color:ink},paragraph:{outlineLevel:0}},{id:'Heading2',name:'Heading 2',basedOn:'Normal',next:'Normal',quickFormat:true,run:{font:'Arial',size:25,bold:true,color:blue},paragraph:{outlineLevel:1}}]},sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1100,bottom:1100,left:1078,right:1078,header:500,footer:500}}},headers:{default:new Header({children:[p('REC INGENIERÍA   |   PROPUESTA COMERCIAL',{run:{size:16,color:muted},border:{bottom:{style:BorderStyle.SINGLE,size:5,color:'C4D2DC',space:7}}})]})},footers:{default:new Footer({children:[new Paragraph({children:[new TextRun({text:'Comunidad Valenciana · 6 de octubre de 2026',size:16,color:muted}),new TextRun({text:'    |    ',size:16,color:muted}),new TextRun({children:[PageNumber.CURRENT],size:16,color:muted})]})]})},children}]});
fs.mkdirSync(path.dirname(output),{recursive:true});
Packer.toBuffer(doc).then(buf=>{fs.writeFileSync(output,buf);process.stdout.write(JSON.stringify({archivo:output,paginas_previstas:data.pages.length})+'\n');});
