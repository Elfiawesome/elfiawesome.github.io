document.addEventListener('DOMContentLoaded', () => {
	const textInput = document.getElementById('text-input');
	const passwordInput = document.getElementById('password-input');
	const encryptBtn = document.getElementById('encrypt-btn');
	const decryptBtn = document.getElementById('decrypt-btn');
	const outputArea = document.getElementById('output-area');
	const statusDiv = document.getElementById('status');

	const crypto = window.crypto.subtle;

	// Helper function to convert a string to an ArrayBuffer
	function strToArrBuf(str) {
		return new TextEncoder().encode(str);
	}

	// Helper function to convert an ArrayBuffer to a string
	function arrBufToStr(buf) {
		return new TextDecoder().decode(buf);
	}

	// Helper function to convert ArrayBuffer to Base64
	function arrBufToBase64(buf) {
		return btoa(String.fromCharCode(...new Uint8Array(buf)));
	}

	// Helper function to convert Base64 to ArrayBuffer
	function base64ToArrBuf(b64) {
		const byteString = atob(b64);
		const bytes = new Uint8Array(byteString.length);
		for (let i = 0; i < byteString.length; i++) {
			bytes[i] = byteString.charCodeAt(i);
		}
		return bytes.buffer;
	}

	/**
	 * Derives a cryptographic key from a password using PBKDF2.
	 * @param {string} password - The user's password.
	 * @param {ArrayBuffer} salt - A random salt.
	 * @returns {Promise<CryptoKey>} - The derived key.
	 */
	async function deriveKey(password, salt) {
		const keyMaterial = await crypto.importKey(
			'raw',
			strToArrBuf(password),
			{ name: 'PBKDF2' },
			false,
			['deriveKey']
		);
		return crypto.deriveKey(
			{
				name: 'PBKDF2',
				salt: salt,
				iterations: 100000, // A good number of iterations
				hash: 'SHA-256',
			},
			keyMaterial,
			{ name: 'AES-GCM', length: 256 },
			true,
			['encrypt', 'decrypt']
		);
	}

	/**
	 * Encrypts plaintext using AES-GCM.
	 */
	async function handleEncrypt() {
		statusDiv.textContent = '';
		const plainText = textInput.value;
		const password = passwordInput.value;

		if (!plainText || !password) {
			statusDiv.textContent = 'Please enter text and a password.';
			return;
		}

		try {
			const salt = window.crypto.getRandomValues(new Uint8Array(16)); // 16-byte salt
			const iv = window.crypto.getRandomValues(new Uint8Array(12));   // 12-byte IV for AES-GCM

			const key = await deriveKey(password, salt);

			const encrypted = await crypto.encrypt(
				{ name: 'AES-GCM', iv: iv },
				key,
				strToArrBuf(plainText)
			);

			// Bundle salt, iv, and ciphertext into one Base64 string for easy transport
			const bundled = `${arrBufToBase64(salt)}.${arrBufToBase64(iv)}.${arrBufToBase64(encrypted)}`;
			outputArea.value = bundled;
			textInput.value = '';

		} catch (error) {
			console.error('Encryption failed:', error);
			statusDiv.textContent = 'Encryption failed. See console for details.';
		}
	}

	/**
	 * Decrypts ciphertext using AES-GCM.
	 */
	async function handleDecrypt() {
		statusDiv.textContent = '';
		const bundledText = textInput.value;
		const password = passwordInput.value;

		if (!bundledText || !password) {
			statusDiv.textContent = 'Please enter encrypted text and a password.';
			return;
		}

		try {
			const parts = bundledText.split('.');
			if (parts.length !== 3) {
				throw new Error('Invalid encrypted data format.');
			}

			const salt = base64ToArrBuf(parts[0]);
			const iv = base64ToArrBuf(parts[1]);
			const encrypted = base64ToArrBuf(parts[2]);

			const key = await deriveKey(password, salt);

			const decrypted = await crypto.decrypt(
				{ name: 'AES-GCM', iv: iv },
				key,
				encrypted
			);

			outputArea.value = arrBufToStr(decrypted);
			textInput.value = '';

		} catch (error) {
			console.error('Decryption failed:', error);
			statusDiv.textContent = 'Decryption failed. Check password or data integrity.';
		}
	}

	encryptBtn.addEventListener('click', handleEncrypt);
	decryptBtn.addEventListener('click', handleDecrypt);
});