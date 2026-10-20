(function(){var c=[].slice.call(document.querySelectorAll('.fs-card')),b=document.getElementById('fs-toggle');
function upd(){b.textContent=c.every(function(d){return d.open})?'Collapse all':'Expand all'}
if(matchMedia('(max-width:600px)').matches)c.forEach(function(d,i){if(i>1)d.open=false});
c.forEach(function(d){d.addEventListener('toggle',upd)});b.onclick=function(){var o=!c.every(function(d){return d.open});c.forEach(function(d){d.open=o});upd()};upd()})();
