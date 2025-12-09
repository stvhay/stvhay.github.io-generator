/**
 * Email Scrambler - A silly but fun way to obfuscate email addresses
 * Uses the email length as a key to create a reversible scramble
 * Animates the unscrambling like solving a puzzle
 */

/**
 * Scrambles an email address using its length as the scrambling key
 * @param {string} email - The email address to scramble
 * @returns {string} The scrambled email address
 */
function scrambleEmail(email) {
  if (!email || typeof email !== "string") {
    return "";
  }

  const chars = email.split("");
  const len = email.length;

  // Create a deterministic permutation based on length
  // We'll use a simple algorithm: swap pairs based on position and length
  for (let i = 0; i < len - 1; i++) {
    // Calculate swap target using length as part of the formula
    const swapTarget = (i + len) % (len - i);
    const j = i + swapTarget;

    // Swap characters
    [chars[i], chars[j]] = [chars[j], chars[i]];
  }

  return chars.join("");
}

/**
 * Generates the sequence of swaps needed to unscramble an email
 * @param {number} length - Length of the email address
 * @returns {Array<[number, number]>} Array of [index1, index2] pairs to swap
 */
function getUnscrambleSwaps(length) {
  const swaps = [];

  // Reverse the scrambling algorithm
  for (let i = length - 2; i >= 0; i--) {
    const swapTarget = (i + length) % (length - i);
    const j = i + swapTarget;
    swaps.push([i, j]);
  }

  return swaps;
}

/**
 * Unscrambles an email with animated "puzzle solving" effect
 * @param {string} scrambled - The scrambled email address
 * @param {HTMLElement} element - The element to animate
 * @param {number} swapDelay - Delay between swaps in milliseconds
 * @returns {Promise<string>} Promise that resolves to the unscrambled email
 */
async function unscrambleEmail(scrambled, element, swapDelay = 80) {
  if (!scrambled || typeof scrambled !== "string") {
    return "";
  }

  const chars = scrambled.split("");
  const swaps = getUnscrambleSwaps(scrambled.length);

  // Animate each swap
  for (const [i, j] of swaps) {
    // Highlight the characters being swapped
    element.innerHTML = chars
      .map((char, idx) => {
        if (idx === i || idx === j) {
          return `<span class="swapping">${char}</span>`;
        }
        return `<span>${char}</span>`;
      })
      .join("");

    // Wait a bit to show the highlight
    await new Promise((resolve) => setTimeout(resolve, swapDelay));

    // Perform the swap
    [chars[i], chars[j]] = [chars[j], chars[i]];

    // Update display with swapped characters
    element.innerHTML = chars
      .map((char) => `<span>${char}</span>`)
      .join("");

    // Small delay between swaps
    await new Promise((resolve) => setTimeout(resolve, swapDelay / 2));
  }

  return chars.join("");
}

/**
 * Sets up a reveal button for a scrambled email
 * @param {string} buttonId - ID of the button element
 * @param {string} emailDisplayId - ID of the element to show the email
 * @param {string} scrambledEmail - The scrambled email address
 * @param {number} swapDelay - Animation speed in milliseconds (default 80)
 */
function setupEmailReveal(buttonId, emailDisplayId, scrambledEmail, swapDelay = 80) {
  const button = document.getElementById(buttonId);
  const emailDisplay = document.getElementById(emailDisplayId);

  if (!button || !emailDisplay) {
    console.error(
      "Email reveal setup failed: button or display element not found",
    );
    return;
  }

  // Initialize with scrambled text
  emailDisplay.textContent = scrambledEmail;
  emailDisplay.classList.add("scrambled");

  // Prevent default link behavior until unscrambled
  emailDisplay.addEventListener("click", function (e) {
    if (emailDisplay.classList.contains("scrambled")) {
      e.preventDefault();
      return false;
    }
  });

  button.addEventListener("click", async function () {
    // Hide button immediately to prevent layout shift during animation
    button.style.display = "none";

    try {
      // Unscramble with animation
      const unscrambled = await unscrambleEmail(
        scrambledEmail,
        emailDisplay,
        swapDelay,
      );

      // Update the link to point to the real email
      emailDisplay.href = `mailto:${unscrambled}`;
      emailDisplay.textContent = unscrambled;
      emailDisplay.classList.remove("scrambled");
      emailDisplay.classList.add("revealed");
    } catch (error) {
      console.error("Error unscrambling email:", error);
      // Show button again with error message if something fails
      button.style.display = "inline-block";
      button.textContent = "Error - Refresh page";
      button.disabled = true;
    }
  });
}

// Export for use in other scripts if needed
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    scrambleEmail,
    unscrambleEmail,
    setupEmailReveal,
  };
}
