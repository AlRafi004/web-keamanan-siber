// Security Tools JavaScript
class SecurityTools {
  constructor() {
    this.initEventListeners();
  }

  initEventListeners() {
    // Password length slider
    const lengthSlider = document.getElementById("password-length");
    const lengthDisplay = document.getElementById("length-display");

    if (lengthSlider && lengthDisplay) {
      lengthSlider.addEventListener("input", (e) => {
        lengthDisplay.textContent = e.target.value;
      });
    }

    // Real-time password checking
    const passwordInput = document.getElementById("password-input");
    if (passwordInput) {
      passwordInput.addEventListener("input", () => {
        if (passwordInput.value.length > 0) {
          this.checkPasswordRealTime(passwordInput.value);
        }
      });
    }

    // Smooth scrolling for navigation
    document.querySelectorAll(".nav-link, .cta-button").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        const target = document.querySelector(link.getAttribute("href"));
        if (target) {
          target.scrollIntoView({
            behavior: "smooth",
            block: "start",
          });
        }
      });
    });
  }

  checkPasswordRealTime(password) {
    const analysis = this.analyzePassword(password);
    this.displayPasswordAnalysis(analysis);
  }
}

// Tool Modal Management
function showTool(toolId) {
  const modal = document.getElementById(toolId);
  if (modal) {
    modal.style.display = "block";
    document.body.style.overflow = "hidden";

    // Add fade-in animation
    modal.style.opacity = "0";
    setTimeout(() => {
      modal.style.opacity = "1";
      modal.style.transition = "opacity 0.3s ease";
    }, 10);
  }
}

function hideTool(toolId) {
  const modal = document.getElementById(toolId);
  if (modal) {
    modal.style.opacity = "0";
    setTimeout(() => {
      modal.style.display = "none";
      document.body.style.overflow = "auto";
    }, 300);
  }
}

// Password Generator
function generatePassword() {
  const length = parseInt(document.getElementById("password-length").value);
  const includeUppercase = document.getElementById("include-uppercase").checked;
  const includeLowercase = document.getElementById("include-lowercase").checked;
  const includeNumbers = document.getElementById("include-numbers").checked;
  const includeSymbols = document.getElementById("include-symbols").checked;
  const excludeAmbiguous = document.getElementById("exclude-ambiguous").checked;

  let charset = "";

  if (includeUppercase) {
    charset += excludeAmbiguous
      ? "ABCDEFGHJKLMNPQRSTUVWXYZ"
      : "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  }

  if (includeLowercase) {
    charset += excludeAmbiguous
      ? "abcdefghijkmnpqrstuvwxyz"
      : "abcdefghijklmnopqrstuvwxyz";
  }

  if (includeNumbers) {
    charset += excludeAmbiguous ? "23456789" : "0123456789";
  }

  if (includeSymbols) {
    charset += "!@#$%^&*()_+-=[]{}|;:,.<>?";
  }

  if (charset === "") {
    alert("Pilih minimal satu jenis karakter!");
    return;
  }

  let password = "";

  // Ensure at least one character from each selected type
  if (includeUppercase) {
    const uppercaseChars = excludeAmbiguous
      ? "ABCDEFGHJKLMNPQRSTUVWXYZ"
      : "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    password +=
      uppercaseChars[Math.floor(Math.random() * uppercaseChars.length)];
  }

  if (includeLowercase) {
    const lowercaseChars = excludeAmbiguous
      ? "abcdefghijkmnpqrstuvwxyz"
      : "abcdefghijklmnopqrstuvwxyz";
    password +=
      lowercaseChars[Math.floor(Math.random() * lowercaseChars.length)];
  }

  if (includeNumbers) {
    const numberChars = excludeAmbiguous ? "23456789" : "0123456789";
    password += numberChars[Math.floor(Math.random() * numberChars.length)];
  }

  if (includeSymbols) {
    const symbolChars = "!@#$%^&*()_+-=[]{}|;:,.<>?";
    password += symbolChars[Math.floor(Math.random() * symbolChars.length)];
  }

  // Fill the remaining length
  for (let i = password.length; i < length; i++) {
    password += charset[Math.floor(Math.random() * charset.length)];
  }

  // Shuffle the password
  password = password
    .split("")
    .sort(() => Math.random() - 0.5)
    .join("");

  document.getElementById("generated-password").value = password;

  // Show password strength
  const strength = analyzePasswordStrength(password);
  displayPasswordStrength(strength);
}

function copyPassword() {
  const passwordField = document.getElementById("generated-password");
  if (passwordField.value) {
    navigator.clipboard
      .writeText(passwordField.value)
      .then(() => {
        const copyButton = document.querySelector(".copy-button");
        const originalText = copyButton.innerHTML;
        copyButton.innerHTML = '<i class="fas fa-check"></i>';
        copyButton.style.background = "#28a745";

        setTimeout(() => {
          copyButton.innerHTML = originalText;
          copyButton.style.background = "#28a745";
        }, 2000);
      })
      .catch(() => {
        // Fallback for older browsers
        passwordField.select();
        document.execCommand("copy");
        alert("Password telah disalin!");
      });
  }
}

// Password Strength Analysis
function analyzePasswordStrength(password) {
  let score = 0;
  let feedback = [];

  // Length check
  if (password.length >= 12) {
    score += 25;
    feedback.push({
      type: "positive",
      message: "Panjang password baik (≥12 karakter)",
    });
  } else if (password.length >= 8) {
    score += 15;
    feedback.push({
      type: "warning",
      message: "Panjang password cukup, lebih baik ≥12 karakter",
    });
  } else {
    feedback.push({
      type: "negative",
      message: "Password terlalu pendek, minimal 8 karakter",
    });
  }

  // Character variety checks
  const checks = [
    { regex: /[a-z]/, points: 15, message: "Mengandung huruf kecil" },
    { regex: /[A-Z]/, points: 15, message: "Mengandung huruf besar" },
    { regex: /[0-9]/, points: 15, message: "Mengandung angka" },
    { regex: /[^a-zA-Z0-9]/, points: 20, message: "Mengandung simbol khusus" },
  ];

  checks.forEach((check) => {
    if (check.regex.test(password)) {
      score += check.points;
      feedback.push({
        type: "positive",
        message: check.message,
      });
    } else {
      feedback.push({
        type: "negative",
        message: `Tidak ${check.message.toLowerCase()}`,
      });
    }
  });

  // Common patterns check
  const commonPatterns = [
    /123456|654321|abcdef|qwerty|password|admin/i,
    /(.)\1{2,}/, // Repeated characters
    /012|123|234|345|456|567|678|789|890/,
    /abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz/i,
  ];

  let hasCommonPattern = false;
  commonPatterns.forEach((pattern) => {
    if (pattern.test(password)) {
      hasCommonPattern = true;
    }
  });

  if (hasCommonPattern) {
    score -= 20;
    feedback.push({
      type: "negative",
      message: "Mengandung pola umum yang mudah ditebak",
    });
  } else {
    feedback.push({
      type: "positive",
      message: "Tidak mengandung pola umum",
    });
  }

  // Entropy calculation (simplified)
  const uniqueChars = new Set(password).size;
  if (uniqueChars / password.length > 0.7) {
    score += 10;
    feedback.push({
      type: "positive",
      message: "Variasi karakter yang baik",
    });
  }

  return {
    score: Math.max(0, Math.min(100, score)),
    feedback: feedback,
  };
}

function displayPasswordStrength(analysis) {
  const strengthDiv = document.getElementById("password-strength");
  let strengthClass = "";
  let strengthText = "";

  if (analysis.score >= 80) {
    strengthClass = "strength-strong";
    strengthText = "Sangat Kuat";
  } else if (analysis.score >= 60) {
    strengthClass = "strength-good";
    strengthText = "Kuat";
  } else if (analysis.score >= 40) {
    strengthClass = "strength-fair";
    strengthText = "Sedang";
  } else if (analysis.score >= 20) {
    strengthClass = "strength-weak";
    strengthText = "Lemah";
  } else {
    strengthClass = "strength-very-weak";
    strengthText = "Sangat Lemah";
  }

  strengthDiv.className = `strength-indicator ${strengthClass}`;
  strengthDiv.innerHTML = `
        <div style="margin-bottom: 1rem;">
            <strong>Kekuatan Password: ${strengthText} (${analysis.score}/100)</strong>
        </div>
        <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 10px; overflow: hidden;">
            <div style="background: rgba(255,255,255,0.8); height: 100%; width: ${analysis.score}%; transition: width 0.5s ease;"></div>
        </div>
    `;
}

// Password Checker
function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password-input");
  const visibilityIcon = document.getElementById("visibility-icon");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    visibilityIcon.className = "fas fa-eye-slash";
  } else {
    passwordInput.type = "password";
    visibilityIcon.className = "fas fa-eye";
  }
}

function checkPassword() {
  const password = document.getElementById("password-input").value;

  if (!password) {
    alert("Masukkan password terlebih dahulu!");
    return;
  }

  const analysis = analyzePassword(password);
  displayPasswordAnalysis(analysis);
}

function analyzePassword(password) {
  const strength = analyzePasswordStrength(password);

  // Additional security checks
  const securityChecks = [
    {
      check: password.length >= 12,
      message: "Minimal 12 karakter",
      icon: password.length >= 12 ? "check" : "times",
    },
    {
      check: /[a-z]/.test(password),
      message: "Mengandung huruf kecil",
      icon: /[a-z]/.test(password) ? "check" : "times",
    },
    {
      check: /[A-Z]/.test(password),
      message: "Mengandung huruf besar",
      icon: /[A-Z]/.test(password) ? "check" : "times",
    },
    {
      check: /[0-9]/.test(password),
      message: "Mengandung angka",
      icon: /[0-9]/.test(password) ? "check" : "times",
    },
    {
      check: /[^a-zA-Z0-9]/.test(password),
      message: "Mengandung simbol khusus",
      icon: /[^a-zA-Z0-9]/.test(password) ? "check" : "times",
    },
    {
      check: !/(.)\1{2,}/.test(password),
      message: "Tidak ada karakter berulang",
      icon: !/(.)\1{2,}/.test(password) ? "check" : "times",
    },
    {
      check: !/123|abc|qwerty|password|admin/i.test(password),
      message: "Tidak mengandung pola umum",
      icon: !/123|abc|qwerty|password|admin/i.test(password)
        ? "check"
        : "times",
    },
  ];

  // Estimated crack time
  let crackTime = "Tidak dapat dihitung";
  if (strength.score >= 80) {
    crackTime = "Jutaan tahun";
  } else if (strength.score >= 60) {
    crackTime = "Ribuan tahun";
  } else if (strength.score >= 40) {
    crackTime = "Puluhan tahun";
  } else if (strength.score >= 20) {
    crackTime = "Beberapa bulan";
  } else {
    crackTime = "Beberapa hari atau kurang";
  }

  return {
    strength: strength,
    securityChecks: securityChecks,
    crackTime: crackTime,
    recommendations: generatePasswordRecommendations(password, securityChecks),
  };
}

function generatePasswordRecommendations(password, securityChecks) {
  const recommendations = [];

  if (password.length < 12) {
    recommendations.push("Perbanyak panjang password minimal 12 karakter");
  }

  if (!/[a-z]/.test(password)) {
    recommendations.push("Tambahkan huruf kecil (a-z)");
  }

  if (!/[A-Z]/.test(password)) {
    recommendations.push("Tambahkan huruf besar (A-Z)");
  }

  if (!/[0-9]/.test(password)) {
    recommendations.push("Tambahkan angka (0-9)");
  }

  if (!/[^a-zA-Z0-9]/.test(password)) {
    recommendations.push("Tambahkan simbol khusus (!@#$%^&*)");
  }

  if (/(.)\1{2,}/.test(password)) {
    recommendations.push("Hindari pengulangan karakter berturut-turut");
  }

  if (/123|abc|qwerty|password|admin/i.test(password)) {
    recommendations.push("Hindari pola dan kata umum yang mudah ditebak");
  }

  if (recommendations.length === 0) {
    recommendations.push("Password Anda sudah sangat baik! Pastikan untuk:");
    recommendations.push(
      "• Tidak menggunakan password yang sama di beberapa akun"
    );
    recommendations.push("• Mengaktifkan two-factor authentication (2FA)");
    recommendations.push("• Mengganti password secara berkala");
    recommendations.push("• Menggunakan password manager");
  }

  return recommendations;
}

function displayPasswordAnalysis(analysis) {
  const analysisDiv = document.getElementById("password-analysis");

  const strengthClass =
    analysis.strength.score >= 80
      ? "strength-strong"
      : analysis.strength.score >= 60
      ? "strength-good"
      : analysis.strength.score >= 40
      ? "strength-fair"
      : analysis.strength.score >= 20
      ? "strength-weak"
      : "strength-very-weak";

  const strengthText =
    analysis.strength.score >= 80
      ? "Sangat Kuat"
      : analysis.strength.score >= 60
      ? "Kuat"
      : analysis.strength.score >= 40
      ? "Sedang"
      : analysis.strength.score >= 20
      ? "Lemah"
      : "Sangat Lemah";

  analysisDiv.innerHTML = `
        <div class="strength-indicator ${strengthClass}">
            <strong>Kekuatan Password: ${strengthText} (${
    analysis.strength.score
  }/100)</strong>
            <div style="background: rgba(255,255,255,0.3); border-radius: 10px; height: 10px; overflow: hidden; margin-top: 0.5rem;">
                <div style="background: rgba(255,255,255,0.8); height: 100%; width: ${
                  analysis.strength.score
                }%; transition: width 0.5s ease;"></div>
            </div>
        </div>
        
        <h4><i class="fas fa-clipboard-check"></i> Analisis Keamanan:</h4>
        <ul>
            ${analysis.securityChecks
              .map(
                (check) => `
                <li>
                    <i class="fas fa-${check.icon} ${
                  check.check ? "check" : "times"
                }"></i>
                    ${check.message}
                </li>
            `
              )
              .join("")}
        </ul>
        
        <div style="margin-top: 1rem; padding: 1rem; background: #e7f3ff; border-radius: 8px; border-left: 4px solid #007bff;">
            <strong><i class="fas fa-clock"></i> Estimasi Waktu Pemecahan:</strong>
            <p style="margin: 0.5rem 0 0 0; font-weight: 600; color: #007bff;">${
              analysis.crackTime
            }</p>
        </div>
        
        <div style="margin-top: 1rem; padding: 1rem; background: #fff3cd; border-radius: 8px; border-left: 4px solid #ffc107;">
            <h5><i class="fas fa-lightbulb"></i> Rekomendasi Perbaikan:</h5>
            <ul style="margin-bottom: 0;">
                ${analysis.recommendations
                  .map((rec) => `<li>${rec}</li>`)
                  .join("")}
            </ul>
        </div>
    `;
}

// URL Safety Checker
function checkURL() {
  const url = document.getElementById("url-input").value;

  if (!url) {
    alert("Masukkan URL terlebih dahulu!");
    return;
  }

  const analysis = analyzeURL(url);
  displayURLAnalysis(analysis);
}

function analyzeURL(url) {
  let riskScore = 0;
  const warnings = [];
  const suggestions = [];

  try {
    const urlObj = new URL(url);

    // Protocol check
    if (urlObj.protocol === "http:") {
      riskScore += 30;
      warnings.push("URL menggunakan HTTP (tidak terenkripsi)");
      suggestions.push("Pastikan website mendukung HTTPS");
    } else if (urlObj.protocol === "https:") {
      suggestions.push("✓ Menggunakan HTTPS (terenkripsi)");
    }

    // Domain checks
    const domain = urlObj.hostname.toLowerCase();

    // Suspicious TLDs
    const suspiciousTLDs = [
      ".tk",
      ".ml",
      ".ga",
      ".cf",
      ".click",
      ".download",
      ".zip",
    ];
    if (suspiciousTLDs.some((tld) => domain.endsWith(tld))) {
      riskScore += 25;
      warnings.push(
        "Domain menggunakan TLD yang sering digunakan untuk phishing"
      );
    }

    // IP address instead of domain
    if (/^\d+\.\d+\.\d+\.\d+$/.test(domain)) {
      riskScore += 40;
      warnings.push("URL menggunakan alamat IP langsung (sangat mencurigakan)");
    }

    // Subdomain checks
    const subdomains = domain.split(".");
    if (subdomains.length > 4) {
      riskScore += 15;
      warnings.push("Terlalu banyak subdomain (mungkin typosquatting)");
    }

    // Suspicious keywords in domain
    const suspiciousKeywords = [
      "secure",
      "bank",
      "paypal",
      "amazon",
      "google",
      "microsoft",
      "apple",
      "login",
      "verify",
      "account",
      "update",
    ];
    const domainLower = domain.toLowerCase();
    suspiciousKeywords.forEach((keyword) => {
      if (
        domainLower.includes(keyword) &&
        !isLegitimateService(domainLower, keyword)
      ) {
        riskScore += 20;
        warnings.push(
          `Domain mengandung kata kunci mencurigakan: "${keyword}"`
        );
      }
    });

    // URL shorteners
    const shorteners = [
      "bit.ly",
      "tinyurl.com",
      "t.co",
      "goo.gl",
      "short.link",
      "ow.ly",
    ];
    if (shorteners.some((shortener) => domain.includes(shortener))) {
      riskScore += 15;
      warnings.push("URL pendek - hati-hati dengan tujuan sebenarnya");
      suggestions.push(
        "Gunakan layanan URL expander untuk melihat tujuan asli"
      );
    }

    // Homograph attacks (visual spoofing)
    if (containsSuspiciousCharacters(domain)) {
      riskScore += 35;
      warnings.push(
        "Domain mengandung karakter yang mirip huruf latin (kemungkinan spoofing)"
      );
    }

    // Path analysis
    const path = urlObj.pathname;
    if (
      path.includes("login") ||
      path.includes("signin") ||
      path.includes("verify")
    ) {
      if (riskScore > 20) {
        riskScore += 20;
        warnings.push(
          "URL mengarah ke halaman login dari domain yang mencurigakan"
        );
      }
    }

    // Query parameters
    if (urlObj.search) {
      const params = new URLSearchParams(urlObj.search);
      if (params.has("redirect") || params.has("return") || params.has("url")) {
        riskScore += 10;
        warnings.push(
          "URL mengandung parameter redirect (hati-hati dengan open redirect)"
        );
      }
    }
  } catch (e) {
    riskScore += 50;
    warnings.push("URL tidak valid atau format yang tidak dikenal");
  }

  // Generate overall assessment
  let riskLevel = "Rendah";
  let riskColor = "#28a745";

  if (riskScore >= 60) {
    riskLevel = "Sangat Tinggi";
    riskColor = "#dc3545";
  } else if (riskScore >= 40) {
    riskLevel = "Tinggi";
    riskColor = "#fd7e14";
  } else if (riskScore >= 20) {
    riskLevel = "Sedang";
    riskColor = "#ffc107";
  }

  return {
    url: url,
    riskScore: Math.min(100, riskScore),
    riskLevel: riskLevel,
    riskColor: riskColor,
    warnings: warnings,
    suggestions: suggestions,
  };
}

function isLegitimateService(domain, keyword) {
  const legitimateDomains = {
    google: ["google.com", "google.co.id", "googleapis.com"],
    microsoft: ["microsoft.com", "office.com", "outlook.com", "live.com"],
    amazon: ["amazon.com", "amazon.co.id", "aws.amazon.com"],
    paypal: ["paypal.com", "paypal.co.id"],
    apple: ["apple.com", "icloud.com"],
    bank: [], // Most bank keywords are suspicious unless exact match
  };

  if (legitimateDomains[keyword]) {
    return legitimateDomains[keyword].some((legitDomain) =>
      domain.endsWith(legitDomain)
    );
  }

  return false;
}

function containsSuspiciousCharacters(domain) {
  // Check for homograph attacks (Cyrillic, mixed scripts, etc.)
  const suspiciousPatterns = [
    /[а-я]/i, // Cyrillic
    /[αβγδεζηθικλμνξοπρστυφχψω]/i, // Greek
    /[àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ]/i, // Extended Latin
  ];

  return suspiciousPatterns.some((pattern) => pattern.test(domain));
}

function displayURLAnalysis(analysis) {
  const analysisDiv = document.getElementById("url-analysis");

  analysisDiv.innerHTML = `
        <div style="padding: 1rem; border-radius: 10px; background: ${
          analysis.riskColor
        }15; border-left: 4px solid ${analysis.riskColor};">
            <h4 style="color: ${analysis.riskColor}; margin-bottom: 0.5rem;">
                <i class="fas fa-shield-alt"></i> 
                Tingkat Risiko: ${analysis.riskLevel} (${
    analysis.riskScore
  }/100)
            </h4>
            <div style="background: ${
              analysis.riskColor
            }20; border-radius: 10px; height: 10px; overflow: hidden;">
                <div style="background: ${
                  analysis.riskColor
                }; height: 100%; width: ${
    analysis.riskScore
  }%; transition: width 0.5s ease;"></div>
            </div>
        </div>
        
        ${
          analysis.warnings.length > 0
            ? `
        <div style="margin-top: 1rem; padding: 1rem; background: #f8d7da; border-radius: 8px; border-left: 4px solid #dc3545;">
            <h5><i class="fas fa-exclamation-triangle"></i> Peringatan:</h5>
            <ul style="margin-bottom: 0;">
                ${analysis.warnings
                  .map(
                    (warning) => `<li style="color: #721c24;">${warning}</li>`
                  )
                  .join("")}
            </ul>
        </div>
        `
            : ""
        }
        
        ${
          analysis.suggestions.length > 0
            ? `
        <div style="margin-top: 1rem; padding: 1rem; background: #d1ecf1; border-radius: 8px; border-left: 4px solid #17a2b8;">
            <h5><i class="fas fa-info-circle"></i> Informasi:</h5>
            <ul style="margin-bottom: 0;">
                ${analysis.suggestions
                  .map(
                    (suggestion) =>
                      `<li style="color: #0c5460;">${suggestion}</li>`
                  )
                  .join("")}
            </ul>
        </div>
        `
            : ""
        }
        
        <div style="margin-top: 1rem; padding: 1rem; background: #e2e3e5; border-radius: 8px;">
            <h5><i class="fas fa-lightbulb"></i> Tips Keamanan URL:</h5>
            <ul style="margin-bottom: 0;">
                <li>Selalu periksa URL sebelum memasukkan data pribadi</li>
                <li>Pastikan URL dimulai dengan "https://" untuk situs yang meminta data sensitif</li>
                <li>Waspada terhadap URL yang sangat panjang atau mengandung banyak parameter</li>
                <li>Periksa ejaan domain - hati-hati dengan typosquatting</li>
                <li>Jangan klik link dari email yang mencurigakan</li>
                <li>Gunakan bookmark untuk situs penting seperti internet banking</li>
            </ul>
        </div>
    `;
}

// Close modal when clicking outside
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("tool-modal")) {
    const modalId = e.target.id;
    hideTool(modalId);
  }
});

// Keyboard shortcuts
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    // Close any open modal
    const openModal = document.querySelector('.tool-modal[style*="block"]');
    if (openModal) {
      hideTool(openModal.id);
    }
  }
});

// Initialize the security tools
document.addEventListener("DOMContentLoaded", () => {
  new SecurityTools();

  // Add smooth animations on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
      }
    });
  }, observerOptions);

  // Observe all cards for animation
  document.querySelectorAll(".tool-card, .education-card").forEach((card) => {
    card.style.opacity = "0";
    card.style.transform = "translateY(30px)";
    card.style.transition = "opacity 0.6s ease, transform 0.6s ease";
    observer.observe(card);
  });
});

// Utility functions for enhanced security
function sanitizeInput(input) {
  return input.replace(/[<>\"']/g, "");
}

function validateURL(url) {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}

// Export functions for testing (if needed)
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    analyzePasswordStrength,
    analyzeURL,
    generatePassword,
    SecurityTools,
  };
}
