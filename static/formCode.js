function reset_filter()
{
	//sets teh specialFlag value to Reset
	var x=document.getElementById("specialFlag");
	x.value="reset";
}

function view_results()
{
	//sets special flag to value view
	var x=document.getElementById("specialFlag");
	x.value="view";
}

function add_filter()
{
	//sets special flag to add
	var x=document.getElementById("specialFlag");
	x.value="add";
	
	if (filter!=""){
		alert(filter);
		alert(conds);
		alert("NOOT EMPTY");
		}
	else{
		alert("EMPTY!");
		}

}
