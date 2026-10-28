(function(){
  // Mobile sidebar toggle
  var btn=document.querySelector('.menu-btn'), side=document.querySelector('.sidebar');
  if(btn&&side){btn.addEventListener('click',function(){side.classList.toggle('open')});
    side.addEventListener('click',function(e){if(e.target.tagName==='A')side.classList.remove('open')});}

  // Search
  var index=window.DIALMIO_INDEX||[];
  function norm(s){return (s||'').toLowerCase()}
  function search(q){
    q=norm(q).trim(); if(!q) return [];
    var words=q.split(/\s+/);
    return index.map(function(it){
      var t=norm(it.t), body=norm(it.k+' '+it.p);
      var score=0;
      for(var i=0;i<words.length;i++){var w=words[i];
        if(t.indexOf(w)>-1) score+=5; else if(body.indexOf(w)>-1) score+=1; else return null;}
      return {it:it,score:score};
    }).filter(Boolean).sort(function(a,b){return b.score-a.score}).slice(0,10).map(function(r){return r.it});
  }
  document.querySelectorAll('[data-search]').forEach(function(box){
    var input=box.querySelector('input'), out=box.querySelector('.results'), sel=-1;
    function render(){
      var res=search(input.value); sel=-1;
      if(!input.value.trim()){out.classList.remove('show');return}
      out.innerHTML=res.length?res.map(function(r){
        return '<a href="'+r.u+'">'+r.t+'<small>'+r.p+'</small></a>'}).join('')
        :'<div class="none">No results. Try "auto dialer", "WhatsApp", "backup", "pricing"…</div>';
      out.classList.add('show');
    }
    input.addEventListener('input',render);
    input.addEventListener('focus',render);
    input.addEventListener('keydown',function(e){
      var links=out.querySelectorAll('a'); if(!links.length) return;
      if(e.key==='ArrowDown'){sel=Math.min(sel+1,links.length-1);e.preventDefault()}
      else if(e.key==='ArrowUp'){sel=Math.max(sel-1,0);e.preventDefault()}
      else if(e.key==='Enter'){location.href=links[Math.max(sel,0)].href;return}
      else return;
      links.forEach(function(l,i){l.classList.toggle('active',i===sel)});
    });
    document.addEventListener('click',function(e){if(!box.contains(e.target))out.classList.remove('show')});
  });
})();
