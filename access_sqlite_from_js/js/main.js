function init() {
	console.log("init Start.");
	console.log("init End.");
}

function onClickAddRow() {

	let table2 = $("#table2 tbody");
	console.log(table2);
	console.log(table2.children());
	console.log(table2.children().length);

	$.each(table2, function(){
		// console.log($(this).html());
		console.log($(this).find(".td1").text());
	})

	// タグをベタ打ちして要素追加
	// mainTable.append("<tr><td>xyz</td></tr>")

	// DOMを生成して要素追加
	let tr = $("<tr>");
	let td1 = $("<td>");
	td1.text("てきすと1");
	let td2 = $("<td>");
	td2.text("てきすと2");
	let td3 = $("<td>");
	td3.text("てきすと3");
	let td4 = $("<td>");
	td4.text("てきすと4");
	tr.append(td1);
	tr.append(td2);
	tr.append(td3);
	tr.append(td4);
	table2.append(tr);
}

function onClickShowTable() {
	execDbAccess().then(function(){
		console.log("execDbAccessの処理完了後にこれが呼ばれる")
	});
	console.log("execDbAccessの処理完了を待たずにこれが呼ばれる")
}

async function execDbAccess() {
	console.log("execDbAccess Start.");

	const sqlPromise = initSqlJs({
		locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.5.0/${file}`
	});
	let sqlFilePath = "../main.db";
	const dataPromise = fetch(sqlFilePath).then(res => res.arrayBuffer());
	const [SQL, buf] = await Promise.all([sqlPromise, dataPromise]);
	const db = new SQL.Database(new Uint8Array(buf));
	let query = "SELECT * FROM CHANNEL";
	let contents = db.exec(query);
	console.log(contents);
	console.log(contents[0]);

	for (const rowOrgin of contents[0].values) {
		row = convertIndexToColId(contents[0].columns, rowOrgin);
		// console.log(rowOrgin);
		// console.log(rowOrgin[0]);
		// console.log(rowOrgin[1]);
		// console.log(rowOrgin[2]);

		console.log(row);
		console.log(row["CHANNEL_ID"]);
		console.log(row["CHANNEL_TITLE"]);
		console.log(row["CHANNEL_CATEGORY1"]);
		console.log(row["CHANNEL_CATEGORY2"]);
		console.log(row["CHANNEL_CATEGORY3"]);
		break;
	}

	console.log("execDbAccess end.");
}

function convertIndexToColId(columns, rowOrigin) {
	
	// console.log(columns);
	// console.log(rowOrigin);

	result = {}
	for (let i=0;i<columns.length;i++) {
		result[columns[i]] = rowOrigin[i];
	}
	// console.log(result);

	return result;
}