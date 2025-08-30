document.addEventListener('DOMContentLoaded', main);

const fileExtData = {};
initializeFileExtData();

const contentElement = document.getElementById('main-content');
const sidebarListElement = document.getElementById('sidebar-list');

async function main() {
	// Form Elements
	const filesTitleElement = document.getElementById('files-title');
	filesTitleElement.addEventListener('click', toggleLoginContainer);

	const loadVaultButton = document.getElementById('load-vault-btn');
	const cancelVaultButton = document.getElementById('cancel-vault-btn');
	loadVaultButton.addEventListener('click', async function (event) {
		event.preventDefault();
		const vaultLinkInput = document.getElementById('vault-link-input');
		const passwordInput = document.getElementById('password-input');
		await updatePage(vaultLinkInput.value, passwordInput.value);
		toggleLoginContainer();
	});
	cancelVaultButton.addEventListener('click', async function (event) {
		event.preventDefault();
		toggleLoginContainer();
	});
}

async function updatePage(vaultLink, password) {
	const indexData = await getVaultIndex(vaultLink, password);

	const filesData = indexData['Files'];
	const VaultsData = indexData['Vaults'];
	const IdCounter = indexData['IdCounter'];

	// Reset sidebar
	sidebarListElement.innerHTML = '';

	// Add back button
	const prevVaultButtonElement = createSideBarItem('🔙', '');
	sidebarListElement.appendChild(prevVaultButtonElement);
	prevVaultButtonElement.addEventListener('click', async function () {
		const prevLink = vaultLink.split('/').slice(0, -1).join('/');
		updatePage(prevLink, password);
	});

	// Add vaults and files
	for (const vaultId in VaultsData) {
		const vault = VaultsData[vaultId];

		const vaultName = vault['Name'];
		const vaultDescription = vault['Description'];

		const listElement = createSideBarItem('📁', vaultName);
		sidebarListElement.appendChild(listElement);

		listElement.addEventListener('click', async function () {
			const newVaultLink = vaultLink + '/' + vaultId;
			updatePage(newVaultLink, password);
		});
	}

	for (const fileId in filesData) {
		const file = filesData[fileId];

		const dateArchived = file['DateArchived'];
		const encryptedPaths = file['EncryptedFilePaths'];
		const fileName = file['Name'];
		const fileDescription = file['Description'];

		const listElement = createSideBarItem(fileExtToEmojiIcon(fileName), fileName);
		sidebarListElement.appendChild(listElement);

		listElement.addEventListener('click', async function () {
			var fileData;
			if (encryptedPaths.length > 1) {
				const fileDataParts = [];
				var totalLength = 0;
				for (const encryptedPath of encryptedPaths) {
					const fileDataPart = await getFile(vaultLink, encryptedPath, password);
					totalLength += fileDataPart.byteLength;
					fileDataParts.push(fileDataPart);
				}

				const combinedArray = new Uint8Array(totalLength);
				var offset = 0;
				for (const fileDataPart of fileDataParts) {
					combinedArray.set(new Uint8Array(fileDataPart), offset)
					offset += fileDataPart.byteLength;
				}

				fileData = combinedArray.buffer;
			} else {
				fileData = await getFile(vaultLink, encryptedPaths[0], password);
			}

			// Clear previous content
			contentElement.innerHTML = '';
			// Add header content
			const headerElement = document.createElement('h2');
			headerElement.textContent = fileName;
			contentElement.appendChild(headerElement);
			// Add media
			switch (fileExtToViewTypeIcon(fileName)) {
				case 'image':
					var blob = new Blob([fileData], { type: 'image/*' });
					const imageUrl = URL.createObjectURL(blob);
					const imageElement = document.createElement('img');
					imageElement.src = imageUrl;
					imageElement.alt = fileName;
					contentElement.appendChild(imageElement);
					break;
				case 'video':
					var blob = new Blob([fileData], { type: 'video/*' });
					const videoUrl = URL.createObjectURL(blob);
					const videoElement = document.createElement('video');
					videoElement.controls = true;
					videoElement.src = videoUrl;
					contentElement.appendChild(videoElement);
					break;
				case 'audio':
					var blob = new Blob([fileData], { type: 'audio/*' });
					const audioUrl = URL.createObjectURL(blob);
					const audioElement = document.createElement('audio');
					audioElement.controls = true;
					audioElement.src = audioUrl;
					contentElement.appendChild(audioElement);
					break;
				case 'code':
					const decoder = new TextDecoder();
					const codeText = decoder.decode(fileData);
					const codeElement = document.createElement('pre');
					codeElement.className = 'code-block';
					codeElement.textContent = codeText;
					contentElement.appendChild(codeElement);
					break;
				default:
					const defaultElement = document.createElement('p');
					defaultElement.textContent = 'Preview not available for this file type. Please download to view.';

					const defaultMediaElement = document.createElement('pre');
					defaultMediaElement.textContent = (new TextDecoder()).decode(fileData);

					contentElement.appendChild(defaultElement);
					contentElement.appendChild(defaultMediaElement);
			}
			// Add description
			const descElement = document.createElement('p');
			descElement.textContent = fileDescription;
			contentElement.appendChild(descElement);
		});
	}
}

async function getFile(vaultLink, fileName, password) {
	const key = await deriveKey(password);
	const response = await fetch(vaultLink + "/" + fileName);

	const buffer = await response.arrayBuffer();
	const decryptedData = await decrypt(buffer, key);
	return decryptedData;
}

async function getVaultIndex(fileLink, password) {
	const indexFileName = "index.vault";

	const key = await deriveKey(password);
	const response = await fetch(fileLink + "/" + indexFileName);

	const buffer = await response.arrayBuffer()
	const decryptedData = await decrypt(buffer, key);

	const decoder = new TextDecoder();
	const indexJson = decoder.decode(decryptedData);

	const index = JSON.parse(indexJson);
	return index;
}


// Decription Utility Function
async function deriveKey(password) {
	const encoder = new TextEncoder();
	const passwordBuffer = encoder.encode(password);
	const hashBuffer = await crypto.subtle.digest('SHA-256', passwordBuffer);
	return crypto.subtle.importKey(
		'raw', hashBuffer, { name: 'AES-CBC' }, false, ['decrypt']
	);
}

async function decrypt(encryptedData, key) {
	const iv = encryptedData.slice(0, 16);
	const ciphertext = encryptedData.slice(16);
	return crypto.subtle.decrypt({ name: 'AES-CBC', iv }, key, ciphertext);
}

// Helper builder Fucntions
function fileNameToExt(fileName) {
	fileName = fileName.toLowerCase();
	return fileName.split('.').pop();
}

function fileExtToViewTypeIcon(fileName) {
	return fileExtData[fileNameToExt(fileName)]?.viewType ?? 'text';
}

function fileExtToEmojiIcon(fileName) {
	return fileExtData[fileNameToExt(fileName)]?.emoji ?? '📄';
}

function createSideBarItem(icon, name) {
	const _li = document.createElement('li');
	const _a = document.createElement('a');
	_a.class = 'file-link';
	_a.textContent = `${icon} ${name}`;
	_li.appendChild(_a);
	return _li;
}

function initializeFileExtData() {
	['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'].forEach(function (ext) {
		fileExtData[ext] = { emoji: '📸', viewType: 'image' };
	});
	['mp4', 'mov', 'avi', 'mkv', 'webm'].forEach(function (ext) {
		fileExtData[ext] = { emoji: '🎬', viewType: 'video' };
	});
	['mp3', 'wav', 'ogg', 'flac'].forEach(function (ext) {
		fileExtData[ext] = { emoji: '🔊', viewType: 'audio' };
	});
	['txt', 'json', 'html'].forEach(function (ext) {
		fileExtData[ext] = { emoji: '📄', viewType: 'code' };
	});
}

function toggleLoginContainer() {
	const loginContainerElement = document.querySelector('.login-container');

	if (loginContainerElement.style.display != 'block') {
		loginContainerElement.style.display = 'block';
	} else {
		loginContainerElement.style.display = 'none';
	}
}