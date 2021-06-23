// this is neccsary because at the time of writing this project sveltekit is in beta
// so for reason after running npm run build it doesn't clean thhe previous build
// :)

const fs = require('fs');
if (fs.existsSync('build/_app')) {
	fs.rmdirSync('build/_app', { recursive: true });
	console.log('cleaned the previous build');
}
