const path=require('node:path');
const PptxGenJS=require('pptxgenjs');
const out=path.resolve(__dirname,'../materiales_comerciales');
async function main(){
  const p=new PptxGenJS();
  p.defineLayout({name:'TARJETA',width:91/25.4,height:61/25.4});
  p.layout='TARJETA';p.author='REC Ingeniería';p.company='REC Ingeniería';
  p.subject='Tarjeta Materia precisa, dos caras con sangrado de 3 mm';
  p.title='REC Ingeniería | Tarjeta Materia precisa';p.lang='es-ES';
  for(const name of ['tarjeta-frente','tarjeta-reverso']){
    const s=p.addSlide();
    s.addImage({path:path.join(out,name+'.svg'),x:0,y:0,w:91/25.4,h:61/25.4,
      altText:name==='tarjeta-frente'?'REC Ingeniería, del terreno al proyecto':
        'Richard Castro Núñez, contactos de España y Chile y QR a recingenieria.com'});
    s.addNotes('REC Ingeniería. Corte 85 × 55 mm, archivo 91 × 61 mm, con sangrado de 3 mm. Imagen conceptual. Contacto digital a recingenieria.com.');
  }
  await p.writeFile({fileName:path.join(out,'REC-tarjeta-91x61-con-sangrado.pptx')});
  const {execFileSync}=require('node:child_process');
  const check=path.join(__dirname,'verificar-tarjeta-pptx.py');
  if(process.env.REC_PYTHON){execFileSync(process.env.REC_PYTHON,[check],{stdio:'inherit'});}
  else{execFileSync('py',['-3.12',check],{stdio:'inherit'});}
  console.log('PowerPoint de dos caras actualizado, con SVG vectorial y respaldo PNG.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
