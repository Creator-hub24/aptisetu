(function(){var p=new URLSearchParams(location.search),pick=document.getElementById('exam-pick'),setup=document.getElementById('setup');
function gen(){pick.classList.add('hidden');setup.classList.remove('hidden');if(window.__quizSetupHook)window.__quizSetupHook(p.get('topic'));}
document.getElementById('pick-general').onclick=gen;
document.getElementById('change-track').onclick=function(e){e.preventDefault();setup.classList.add('hidden');pick.classList.remove('hidden');};
if(p.get('exam')==='general'||p.get('section')){pick.classList.add('hidden');setup.classList.remove('hidden');}})();
