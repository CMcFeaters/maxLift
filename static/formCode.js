function reset_filter()
{
	//sets teh specialFlag value to Reset
	var x=document.getElementById("navFlag");
	x.value="reset";
}

function view_results()
{
	//sets special flag to value view
	var x=document.getElementById("navFlag");
	x.value="view";
}

function add_filter()
{
	//sets special flag to add
	var x=document.getElementById("navFlag");
	x.value="add";
}


function andor()
{
	
	if (numCond>=0)
	{
		//set our the filter addition type and condNum to expand the 0th filter param
		document.getElementById('addType').value="add";
		//add the andor element to the only place it applies
		x=document.getElementById('andorDiv');

		andor=document.createElement("select");
		andor.name="andorP";
		andor.id="andorP";
		
		opA=document.createElement('option');
		opA.value="and_";
		opA.innerHTML="AND";
		andor.appendChild(opA);
		
		opO=document.createElement('option');
		opO.value="or_";
		opO.innerHTML="OR";
		andor.appendChild(opO);
		//append it
		x.appendChild(andor);
	}
	else if (numCond==-1)
	{
		document.getElementByID('addType').value="first";
	}
}
			

