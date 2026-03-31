import re

with open("webpage_design.html", "r", encoding="utf-8") as f:
    html = f.read()

# ── 1. Title + meta ──
html = html.replace(
    "<title>How Auctions Can Distribute Risks More Equitably and Maximise Benefits </title>",
    "<title>Renewable Energy Policy Tracker — IRENA</title>"
)

# ── 2. D3 + TopoJSON + CSS → inject before </head> ──
head_inject = """
<script src="https://cdn.jsdelivr.net/npm/d3@7.9.0/dist/d3.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js"></script>
<style id="tracker-styles">
:root{--irena-blue:#003F73;--irena-teal:#00A3E0;--irena-teal-light:#E6F5FC;--irena-grey-bg:#F5F5F5;--irena-grey-mid:#D0D0D0;--irena-grey-dark:#555;--radius:4px;--shadow:0 2px 8px rgba(0,0,0,.10);}
.pt-stats-bar{display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap;}
.pt-stat-card{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:14px 20px;flex:1;min-width:130px;border-top:3px solid var(--irena-teal);}
.pt-stat-card .sv{font-size:28px;font-weight:700;color:var(--irena-blue);line-height:1;}
.pt-stat-card .sl{font-size:11px;color:var(--irena-grey-dark);text-transform:uppercase;letter-spacing:.08em;margin-top:4px;}
.pt-filters{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:16px 20px;margin-bottom:20px;display:flex;gap:12px;align-items:flex-end;flex-wrap:wrap;}
.pt-fg{display:flex;flex-direction:column;gap:4px;flex:1;min-width:130px;}
.pt-fg label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:var(--irena-grey-dark);}
.pt-fg select,.pt-fg input{border:1px solid var(--irena-grey-mid);border-radius:var(--radius);padding:7px 10px;font-size:13px;background:#fff;width:100%;height:34px;outline:none;transition:border-color .15s;font-family:inherit;}
.pt-fg select:focus,.pt-fg input:focus{border-color:var(--irena-teal);}
.pt-fg.pt-search{flex:2;min-width:200px;}
.pt-search-wrap{position:relative;}
.pt-search-wrap::before{content:"\u2315";position:absolute;left:9px;top:50%;transform:translateY(-50%);color:var(--irena-grey-mid);font-size:16px;pointer-events:none;}
.pt-search-wrap input{padding-left:32px;}
.pt-btn-clear{background:none;border:1px solid var(--irena-grey-mid);border-radius:var(--radius);padding:7px 14px;font-size:12px;cursor:pointer;color:var(--irena-grey-dark);height:34px;white-space:nowrap;transition:all .15s;align-self:flex-end;font-family:inherit;}
.pt-btn-clear:hover{border-color:var(--irena-teal);color:var(--irena-teal);}
.pt-country-bar{display:none;background:var(--irena-teal-light);border:1px solid var(--irena-teal);border-radius:var(--radius);padding:8px 16px;margin-bottom:16px;font-size:13px;color:var(--irena-blue);align-items:center;gap:12px;}
.pt-country-bar.visible{display:flex;}
.pt-country-bar button{margin-left:auto;background:none;border:none;cursor:pointer;color:var(--irena-teal);font-size:14px;padding:0 4px;}
.pt-map-card{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;margin-bottom:20px;}
.pt-map-card h2{font-size:15px;font-weight:600;color:var(--irena-blue);margin-bottom:14px;display:flex;align-items:center;gap:8px;}
.pt-map-card h2 .pt-note{font-size:11px;font-weight:400;color:var(--irena-grey-dark);}
#pt-map-svg{width:100%;height:auto;display:block;}
.pt-country-path{stroke:#fff;stroke-width:.5px;cursor:pointer;transition:opacity .15s;}
.pt-country-path:hover{opacity:.8;}
.pt-country-path.selected{stroke:var(--irena-teal);stroke-width:2px;}
.pt-legend{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-top:12px;}
.pt-legend-label{font-size:11px;color:var(--irena-grey-dark);margin-right:4px;}
.pt-legend-item{display:flex;align-items:center;gap:4px;font-size:11px;color:var(--irena-grey-dark);}
.pt-swatch{width:16px;height:12px;border-radius:2px;border:1px solid rgba(0,0,0,.1);}
#pt-tooltip{position:fixed;background:rgba(0,0,0,.85);color:#fff;padding:8px 12px;border-radius:var(--radius);font-size:12px;pointer-events:none;z-index:9999;display:none;max-width:200px;line-height:1.4;}
#pt-tooltip strong{display:block;font-size:13px;}
.pt-table-card{background:#fff;border-radius:var(--radius);box-shadow:var(--shadow);padding:20px;}
.pt-table-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;flex-wrap:wrap;gap:8px;}
.pt-table-header h2{font-size:15px;font-weight:600;color:var(--irena-blue);}
.pt-table-count{font-size:12px;color:var(--irena-grey-dark);}
.pt-table-count strong{color:var(--irena-blue);}
.pt-table-wrap{overflow-x:auto;}
.pt-table{width:100%;border-collapse:collapse;font-size:13px;}
.pt-table thead th{background:var(--irena-blue);color:#fff;padding:10px 12px;text-align:left;font-weight:600;font-size:12px;white-space:nowrap;cursor:pointer;user-select:none;}
.pt-table thead th:hover{background:#005A9E;}
.pt-table thead th .si{margin-left:4px;opacity:.5;}
.pt-table thead th.sa .si::after{content:" \u25b2";}
.pt-table thead th.sd .si::after{content:" \u25bc";}
.pt-table thead th:not(.sa):not(.sd) .si::after{content:" \u21c5";}
.pt-table tbody tr{border-bottom:1px solid #EEE;transition:background .1s;cursor:pointer;}
.pt-table tbody tr:hover{background:var(--irena-teal-light);}
.pt-table tbody tr.hl{background:#E0F4FD;}
.pt-table tbody td{padding:10px 12px;vertical-align:top;}
.pt-table tbody td.cn{font-weight:600;white-space:nowrap;}
.pt-table tbody td.dc{max-width:300px;color:var(--irena-grey-dark);font-size:12px;}
.badge{display:inline-block;padding:3px 8px;border-radius:12px;font-size:11px;font-weight:600;white-space:nowrap;}
.b-emergency{background:#FDEDEC;color:#922B21;}
.b-target{background:#D6EAF8;color:#1A5276;}
.b-market{background:#D5F5E3;color:#1D6A36;}
.b-existing{background:#E8F8F5;color:#1A6B54;}
.b-analysis{background:#F4ECF7;color:#6C3483;}
.b-mandate{background:#FEF9E7;color:#9A6A00;}
.b-infra{background:#EAF2FF;color:#1B4F99;}
.b-incentive{background:#FEF5E7;color:#A04000;}
.b-finance{background:#EBF5FB;color:#1A5276;}
.pt-src{color:var(--irena-teal);text-decoration:none;font-size:12px;}
.pt-src:hover{text-decoration:underline;}
.pt-pag{display:flex;align-items:center;justify-content:center;gap:6px;margin-top:16px;flex-wrap:wrap;}
.pt-pg-btn{background:#fff;border:1px solid var(--irena-grey-mid);border-radius:var(--radius);padding:5px 12px;font-size:13px;cursor:pointer;transition:all .15s;font-family:inherit;}
.pt-pg-btn:hover{border-color:var(--irena-teal);color:var(--irena-teal);}
.pt-pg-btn.act{background:var(--irena-blue);border-color:var(--irena-blue);color:#fff;}
.pt-pg-btn:disabled{opacity:.4;cursor:default;}
@media(max-width:767px){.pt-stats-bar{gap:10px;}.pt-stat-card{min-width:100px;padding:10px 14px;}.pt-stat-card .sv{font-size:22px;}}
</style>
"""
html = html.replace("</head>", head_inject + "\n</head>")

# ── 3. TopHeader updates ──
html = html.replace(
    "How Auctions Can Distribute Risks More Equitably and Maximise Benefits \n</h1>",
    "Renewable Energy Policy Tracker\n</h1>"
)
html = html.replace(
    'datetime="2026-03-12">12 March 2026',
    'datetime="2026-03-31">31 March 2026'
)
html = html.replace(
    "Expert Insights                            ",
    "Data &amp; Statistics                            "
)
html = html.replace(
    """                            <div class="m-TopHeader__footerRight">
                                <span class="m-TopHeader__authorLabel">Authors:</span>
                                <span class="m-TopHeader__author">
                                     Hannah Sofia Guinto
                                </span>
                            </div>""",
    ""
)

# ── 4. Breadcrumbs ──
html = html.replace(
    '<span itemprop="name">News</span>',
    '<span itemprop="name">Data &amp; Statistics</span>'
)
html = html.replace(
    '<span class="c-Breadcrumbs__text" itemprop="name">Expert Insights</span>',
    '<span class="c-Breadcrumbs__text" itemprop="name">Data Tools</span>'
)
html = html.replace(
    'Maximise Benefits </span>',
    'Renewable Energy Policy Tracker</span>'
)

# ── 5. Replace newsletter+content section with full-width tracker ──
START = '<section class="l-section l-section--container ">\n                <div class="l-grid__row">\n                    <div class="l-grid__xxs--4 l-grid__m--2 set-order-on-mobile ">'
END   = '<div class="l-grid10__m--9 l-grid10__m__offset--1 "'

tracker_html = """<section class="l-section l-section--container ">
<div class="l-grid__row">
  <div class="l-grid__xxs--4 l-grid__m--2 set-order-on-mobile ">
    <div class="m-NewsletterSmallForm show-on-desktop" data-jsmodule="NewsletterSmallForm">
      <div class="Heading "><h4 class="Heading__text ">Newsletter</h4></div>
      <form class="m-NewsletterSmallForm__form" action="https://www.irena.org/subscriptionform" method="post">
        <input type="text" name="EmailId" class="m-NewsletterSmallForm__input" placeholder="Enter e-mail address" aria-label="Subscribe">
        <button type="submit" class="m-NewsletterSmallForm__btn" disabled>Go</button>
      </form>
    </div>
  </div>
  <div class="l-grid__m--10 ">
<div style="padding:0 0 32px 0">

<div class="pt-stats-bar">
  <div class="pt-stat-card"><div class="sv" id="pt-stat-total">\u2014</div><div class="sl">Total Measures</div></div>
  <div class="pt-stat-card"><div class="sv" id="pt-stat-countries">\u2014</div><div class="sl">Countries / Orgs</div></div>
  <div class="pt-stat-card"><div class="sv" id="pt-stat-emergency">\u2014</div><div class="sl">Emergency Measures</div></div>
  <div class="pt-stat-card"><div class="sv" id="pt-stat-sectors">\u2014</div><div class="sl">Sectors</div></div>
</div>

<div class="pt-filters">
  <div class="pt-fg"><label>Region</label>
    <select id="pt-region"><option value="">All Regions</option><option>Africa</option><option>Americas</option><option>Asia-Pacific</option><option>Europe</option><option>International</option><option>Middle East</option></select>
  </div>
  <div class="pt-fg"><label>Sector</label>
    <select id="pt-sector"><option value="">All Sectors</option><option>Biofuels</option><option>Conservation</option><option>Cross-cutting</option><option>Energy Efficiency</option><option>Grid / Storage</option><option>Hydro</option><option>Nuclear</option><option>Solar</option><option>Transport / EVs</option><option>Wind</option></select>
  </div>
  <div class="pt-fg"><label>Policy Type</label>
    <select id="pt-type"><option value="">All Types</option><option>Analysis</option><option>Emergency Measure</option><option>Existing Capacity</option><option>Financing / Strategy</option><option>Incentive</option><option>Infrastructure</option><option>Mandate / Regulation</option><option>Market Response</option><option>Target / Strategy</option></select>
  </div>
  <div class="pt-fg pt-search"><label>Search</label>
    <div class="pt-search-wrap"><input type="text" id="pt-search" placeholder="Country or policy name\u2026"></div>
  </div>
  <button class="pt-btn-clear" id="pt-clear">\u2715 Clear</button>
</div>

<div class="pt-country-bar" id="pt-country-bar">
  Showing measures for <strong id="pt-country-name"></strong>
  <button id="pt-deselect">\u2715 Clear</button>
</div>

<div class="pt-map-card">
  <h2>Policy Distribution by Country <span class="pt-note">\u2014 click a country to filter the table</span></h2>
  <svg id="pt-map-svg" viewBox="0 0 960 480" preserveAspectRatio="xMidYMid meet"></svg>
  <div class="pt-legend">
    <span class="pt-legend-label">Measures:</span>
    <div class="pt-legend-item"><div class="pt-swatch" style="background:#D0D0D0"></div> 0</div>
    <div class="pt-legend-item"><div class="pt-swatch" style="background:#B8DFF5"></div> 1\u20132</div>
    <div class="pt-legend-item"><div class="pt-swatch" style="background:#5AB8E8"></div> 3\u20135</div>
    <div class="pt-legend-item"><div class="pt-swatch" style="background:#0073B7"></div> 6\u20139</div>
    <div class="pt-legend-item"><div class="pt-swatch" style="background:#003F73"></div> 10+</div>
    <div style="margin-left:16px" class="pt-legend-item"><div class="pt-swatch" style="background:#E0F4FD;border:2px solid #00A3E0"></div> Selected</div>
  </div>
</div>

<div class="pt-table-card">
  <div class="pt-table-header">
    <h2>Policy &amp; Measure Details</h2>
    <span class="pt-table-count" id="pt-count"></span>
  </div>
  <div class="pt-table-wrap">
    <table class="pt-table" id="pt-table">
      <thead><tr>
        <th data-col="country">Country / Org<span class="si"></span></th>
        <th data-col="region">Region<span class="si"></span></th>
        <th data-col="policy_name">Policy / Measure<span class="si"></span></th>
        <th data-col="sector">Sector<span class="si"></span></th>
        <th data-col="policy_type">Type<span class="si"></span></th>
        <th data-col="date">Date<span class="si"></span></th>
        <th>Key Details</th>
      </tr></thead>
      <tbody id="pt-tbody"></tbody>
    </table>
  </div>
  <div class="pt-pag" id="pt-pag"></div>
</div>

</div>
  </div><!-- /.l-grid__m--10 -->
</div><!-- /.l-grid__row -->
</section>
<div id="pt-tooltip"></div>

"""

si = html.find(START)
ei = html.find(END)
print(f"START index: {si}, END index: {ei}")
if si == -1 or ei == -1:
    print("ERROR: markers not found")
else:
    html = html[:si] + tracker_html + html[ei:]

# ── 6. Tracker JS before </body> ──
tracker_js = """
<script id="tracker-js">
const PT={all:[],filtered:[],selected:null,sortCol:'country',sortDir:'asc',page:1,pageSize:25,counts:{},iso3name:{}};
const PTCOLORS=[{min:0,max:0,c:'#D0D0D0'},{min:1,max:2,c:'#B8DFF5'},{min:3,max:5,c:'#5AB8E8'},{min:6,max:9,c:'#0073B7'},{min:10,max:Infinity,c:'#003F73'}];
function ptColor(n){for(const b of PTCOLORS)if(n>=b.min&&n<=b.max)return b.c;return'#D0D0D0';}
function ptTypeBadge(t){switch(t){case'Emergency Measure':return'b-emergency';case'Target / Strategy':return'b-target';case'Market Response':return'b-market';case'Existing Capacity':return'b-existing';case'Analysis':return'b-analysis';case'Mandate / Regulation':return'b-mandate';case'Infrastructure':return'b-infra';case'Incentive':return'b-incentive';case'Financing / Strategy':return'b-finance';default:return'b-analysis';}}
function ptEsc(s){return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}

async function ptInit(){
  const[dr,wr]=await Promise.all([fetch('./data.json'),fetch('./world-110m.json')]);
  const data=await dr.json(),world=await wr.json();
  PT.all=data.policies;
  document.getElementById('pt-stat-total').textContent=data.policies.length;
  document.getElementById('pt-stat-countries').textContent=new Set(data.policies.map(p=>p.iso3)).size;
  document.getElementById('pt-stat-emergency').textContent=data.policies.filter(p=>p.policy_type==='Emergency Measure').length;
  document.getElementById('pt-stat-sectors').textContent=new Set(data.policies.map(p=>p.sector)).size;
  ptDrawMap(world);ptApply();
}

function ptDrawMap(world){
  const svg=d3.select('#pt-map-svg');
  const proj=d3.geoNaturalEarth1().scale(153).translate([480,240]);
  const path=d3.geoPath().projection(proj);
  const countries=topojson.feature(world,world.objects.countries);
  const n2i=ptN2I();
  countries.features.forEach(f=>{const i=n2i[f.id];if(i){const m=PT.all.find(p=>p.iso3===i);if(m)PT.iso3name[i]=m.country;}});
  svg.append('path').datum({type:'Sphere'}).attr('d',path).attr('fill','#EAF4FB').attr('stroke','#BFD9EC').attr('stroke-width',.5);
  svg.append('path').datum(d3.geoGraticule()()).attr('d',path).attr('fill','none').attr('stroke','#D5E8F5').attr('stroke-width',.3);
  svg.selectAll('.pt-country-path').data(countries.features).join('path')
    .attr('class','pt-country-path').attr('d',path)
    .attr('data-iso3',d=>n2i[d.id]||'')
    .attr('fill',d=>{const i=n2i[d.id];return ptColor(i?(PT.counts[i]||0):0);})
    .on('mouseover',function(e,d){
      const i=n2i[d.id],nm=i?(PT.iso3name[i]||i):'Unknown',c=i?(PT.counts[i]||0):0;
      const t=document.getElementById('pt-tooltip');
      t.innerHTML='<strong>'+nm+'</strong>'+c+' '+(c===1?'measure':'measures');
      t.style.display='block';
    })
    .on('mousemove',function(e){const t=document.getElementById('pt-tooltip');t.style.left=(e.clientX+14)+'px';t.style.top=(e.clientY-28)+'px';})
    .on('mouseout',()=>document.getElementById('pt-tooltip').style.display='none')
    .on('click',function(e,d){
      const i=n2i[d.id];if(!i)return;
      const c=PT.all.filter(p=>p.iso3===i).length;if(c===0)return;
      if(PT.selected===i)ptDeselect();else ptSelect(i,PT.iso3name[i]||i);
    });
}

function ptUpdateColors(){
  d3.selectAll('.pt-country-path')
    .attr('fill',function(){const i=this.getAttribute('data-iso3'),c=i?(PT.counts[i]||0):0;if(PT.selected&&i===PT.selected)return'#E0F4FD';return ptColor(c);})
    .classed('selected',function(){return this.getAttribute('data-iso3')===PT.selected;});
}
function ptSelect(iso3,name){PT.selected=iso3;document.getElementById('pt-country-name').textContent=name;document.getElementById('pt-country-bar').classList.add('visible');ptUpdateColors();ptApply();}
function ptDeselect(){PT.selected=null;document.getElementById('pt-country-bar').classList.remove('visible');ptUpdateColors();ptApply();}

function ptApply(){
  const reg=document.getElementById('pt-region').value,
        sec=document.getElementById('pt-sector').value,
        typ=document.getElementById('pt-type').value,
        q=document.getElementById('pt-search').value.toLowerCase().trim();
  PT.filtered=PT.all.filter(p=>{
    if(reg&&p.region!==reg)return false;
    if(sec&&p.sector!==sec)return false;
    if(typ&&p.policy_type!==typ)return false;
    if(q&&!p.country.toLowerCase().includes(q)&&!p.policy_name.toLowerCase().includes(q))return false;
    if(PT.selected&&p.iso3!==PT.selected)return false;
    return true;
  });
  PT.counts={};PT.filtered.forEach(p=>{PT.counts[p.iso3]=(PT.counts[p.iso3]||0)+1;});
  PT.page=1;ptUpdateColors();ptRender();
}

function ptRender(){
  const col=PT.sortCol,dir=PT.sortDir==='asc'?1:-1;
  const sorted=[...PT.filtered].sort((a,b)=>{const av=a[col]??'',bv=b[col]??'';return(typeof av==='number'?(av-bv):av.toString().localeCompare(bv.toString()))*dir;});
  const tot=sorted.length,pages=Math.max(1,Math.ceil(tot/PT.pageSize));
  if(PT.page>pages)PT.page=pages;
  const st=(PT.page-1)*PT.pageSize,sl=sorted.slice(st,st+PT.pageSize);
  document.getElementById('pt-count').innerHTML='Showing <strong>'+Math.min(st+1,tot)+'\u2013'+Math.min(st+PT.pageSize,tot)+'</strong> of <strong>'+tot+'</strong> measure'+(tot===1?'':'s');
  const tb=document.getElementById('pt-tbody');
  tb.innerHTML=sl.map(p=>'<tr data-iso3="'+p.iso3+'" class="'+(p.iso3===PT.selected?'hl':'')+'"><td class="cn">'+ptEsc(p.country)+'</td><td>'+ptEsc(p.region)+'</td><td><strong>'+ptEsc(p.policy_name)+'</strong></td><td>'+ptEsc(p.sector)+'</td><td><span class="badge '+ptTypeBadge(p.policy_type)+'">'+ptEsc(p.policy_type)+'</span></td><td style="white-space:nowrap;font-size:12px;color:var(--irena-grey-dark)">'+ptEsc(p.date)+'</td><td class="dc">'+ptEsc(p.quantitative_details)+'</td></tr>').join('');
  tb.querySelectorAll('tr').forEach(row=>row.addEventListener('click',()=>{const i=row.getAttribute('data-iso3');if(!i||i==='INT')return;if(PT.selected===i)ptDeselect();else{const nm=PT.all.find(p=>p.iso3===i)?.country||i;ptSelect(i,nm);}}));
  document.querySelectorAll('#pt-table thead th[data-col]').forEach(th=>{th.classList.remove('sa','sd');if(th.dataset.col===PT.sortCol)th.classList.add(PT.sortDir==='asc'?'sa':'sd');});
  ptPag(pages);
}

function ptPag(pages){
  const el=document.getElementById('pt-pag');
  if(pages<=1){el.innerHTML='';return;}
  let h='<button class="pt-pg-btn" id="pt-prev"'+(PT.page===1?' disabled':'')+'>&#8592; Prev</button>';
  for(let i=1;i<=pages;i++){
    if(pages>7&&Math.abs(i-PT.page)>2&&i!==1&&i!==pages){if(i===2||i===pages-1)h+='<span style="padding:0 4px;color:#aaa">\u2026</span>';continue;}
    h+='<button class="pt-pg-btn'+(i===PT.page?' act':'')+'" data-pg="'+i+'">'+i+'</button>';
  }
  h+='<button class="pt-pg-btn" id="pt-next"'+(PT.page===pages?' disabled':'')+'>Next &#8594;</button>';
  el.innerHTML=h;
  el.querySelector('#pt-prev')?.addEventListener('click',()=>{PT.page--;ptRender();});
  el.querySelector('#pt-next')?.addEventListener('click',()=>{PT.page++;ptRender();});
  el.querySelectorAll('[data-pg]').forEach(b=>b.addEventListener('click',()=>{PT.page=parseInt(b.dataset.pg);ptRender();}));
}

function ptN2I(){return{4:'AFG',8:'ALB',12:'DZA',24:'AGO',32:'ARG',36:'AUS',40:'AUT',50:'BGD',56:'BEL',68:'BOL',76:'BRA',100:'BGR',104:'MMR',116:'KHM',120:'CMR',124:'CAN',144:'LKA',152:'CHL',156:'CHN',170:'COL',180:'COD',188:'CRI',191:'HRV',192:'CUB',196:'CYP',203:'CZE',208:'DNK',218:'ECU',818:'EGY',231:'ETH',246:'FIN',250:'FRA',276:'DEU',288:'GHA',300:'GRC',348:'HUN',356:'IND',360:'IDN',364:'IRN',368:'IRQ',372:'IRL',376:'ISR',380:'ITA',392:'JPN',400:'JOR',398:'KAZ',404:'KEN',410:'KOR',414:'KWT',418:'LAO',484:'MEX',504:'MAR',508:'MOZ',524:'NPL',528:'NLD',554:'NZL',566:'NGA',578:'NOR',512:'OMN',586:'PAK',600:'PRY',604:'PER',608:'PHL',616:'POL',620:'PRT',634:'QAT',642:'ROU',643:'RUS',682:'SAU',686:'SEN',710:'ZAF',724:'ESP',752:'SWE',756:'CHE',764:'THA',792:'TUR',800:'UGA',804:'UKR',784:'ARE',826:'GBR',840:'USA',858:'URY',862:'VEN',704:'VNM',887:'YEM',894:'ZMB',716:'ZWE',458:'MYS',702:'SGP',703:'SVK',705:'SVN',788:'TUN',795:'TKM',834:'TZA',860:'UZB'};}

document.addEventListener('DOMContentLoaded',()=>{
  ['pt-region','pt-sector','pt-type'].forEach(id=>document.getElementById(id)?.addEventListener('change',ptApply));
  document.getElementById('pt-search')?.addEventListener('input',ptApply);
  document.getElementById('pt-clear')?.addEventListener('click',()=>{['pt-region','pt-sector','pt-type'].forEach(id=>{const el=document.getElementById(id);if(el)el.value='';});const s=document.getElementById('pt-search');if(s)s.value='';ptDeselect();});
  document.getElementById('pt-deselect')?.addEventListener('click',ptDeselect);
  document.querySelectorAll('#pt-table thead th[data-col]').forEach(th=>th.addEventListener('click',()=>{const c=th.dataset.col;if(PT.sortCol===c)PT.sortDir=PT.sortDir==='asc'?'desc':'asc';else{PT.sortCol=c;PT.sortDir='asc';}ptRender();}));
  ptInit();
});
</script>
"""

html = html.replace("</body>", tracker_js + "\n</body>")

with open("irena_policy_tracker.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done! irena_policy_tracker.html written successfully.")
