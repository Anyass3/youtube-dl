// this is neccsary because at the time of writing this project sveltekit is in beta
// so for reason after running npm run build it doesn't clean thhe previous build
// :)

const fs = require('fs');
if (fs.existsSync('build/_app')) {
	fs.rmdirSync('build/_app', { recursive: true });
	console.log('cleaned the previous build');
}

if (
	fs.existsSync('src/lib/connectionBuilder.ts') &&
	fs.existsSync('server_endpoint') &&
	fs.readFileSync('server_endpoint', 'utf-8')
) {
	let file = fs.readFileSync('src/lib/connectionBuilder.ts', 'utf-8');
	let server_endpoint = fs.readFileSync('server_endpoint', 'utf-8');
	server_endpoint = server_endpoint.replace(/[\n\t\ ]*/g, '');
	if (!(server_endpoint.includes('"') || server_endpoint.includes("'")))
		server_endpoint = `'${server_endpoint}'`;

	file = file.replace('import.meta.env.VITE_SERVER_ENPOINT', server_endpoint);
	fs.writeFileSync('src/lib/connectionBuilder.ts', file);
	console.log('server_endpoint is from server_endpoint', server_endpoint);
}
