(function(){var box=document.getElementById('sample'),fb=document.getElementById('sample-fb'),bs=[].slice.call(box.querySelectorAll('.mini-opt'));
bs.forEach(function(b){b.onclick=function(){var ok=b.dataset.ok==='1';bs.forEach(function(x){x.disabled=true;if(x.dataset.ok==='1')x.classList.add('right')});if(!ok)b.classList.add('wrong');
fb.innerHTML=(ok?'<b>✅ Correct!</b> ':'<b>❌ Not quite.</b> The answer is B. ')+'Together they finish 1/12 + 1/18 = 5/36 of the job a day, so they need 36/5 = 7.2 days.'+
'<div class="cta-row" style="margin:.8em 0 0"><a class="btn btn-sm" href="practice.html?quick=10">Try a 10-question quick quiz →</a><button type="button" class="btn btn-ghost btn-sm" id="sample-again">Try again</button></div>';
fb.classList.remove('hidden');document.getElementById('sample-again').onclick=function(){bs.forEach(function(x){x.disabled=false;x.classList.remove('right','wrong')});fb.classList.add('hidden')};}});})();
