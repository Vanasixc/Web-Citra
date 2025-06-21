document.addEventListener('DOMContentLoaded', function() {
  const toggleLeftSidebarBtn = document.getElementById('toggleLeftSidebarBtn');
  const toggleRightSidebarBtn = document.getElementById('toggleRightSidebarBtn');
  const leftSidebar = document.getElementById('leftSidebar');
  const rightSidebar = document.getElementById('rightSidebar');
  const mainContent = document.getElementById('main-content');
  
  let leftSidebarOpen = true;
  let rightSidebarOpen = true;
  
  // --- Sidebar Toggle Logic ---
  // Move toggle buttons to be direct siblings for easier CSS management if needed
  if (toggleLeftSidebarBtn && leftSidebar && leftSidebar.parentNode) {
    leftSidebar.parentNode.insertBefore(toggleLeftSidebarBtn, leftSidebar.nextSibling);
  }
  
  if (toggleRightSidebarBtn && rightSidebar && rightSidebar.parentNode) {
     // Place it relative to the body or a main container if rightSidebar is not always present
     // For now, assuming it's okay to append to body if structure is complex
     document.body.appendChild(toggleRightSidebarBtn);
  }
  
  toggleLeftSidebarBtn.addEventListener('click', function() {
    leftSidebarOpen = !leftSidebarOpen;
    leftSidebar.classList.toggle('minimized');
    mainContent.classList.toggle('left-expanded', !leftSidebarOpen); // Add class if minimized
    mainContent.classList.toggle('left-collapsed', leftSidebarOpen); // Add class if open
    toggleLeftSidebarBtn.textContent = leftSidebarOpen ? '⇤' : '⇥';
    // Adjust button position based on sidebar state
    toggleLeftSidebarBtn.style.left = leftSidebarOpen ? '240px' : '20px';
  });
  
  toggleRightSidebarBtn.addEventListener('click', function() {
    rightSidebarOpen = !rightSidebarOpen;
    rightSidebar.classList.toggle('minimized');
    mainContent.classList.toggle('right-expanded', !rightSidebarOpen); // Add class if minimized
    mainContent.classList.toggle('right-collapsed', rightSidebarOpen); // Add class if open
    toggleRightSidebarBtn.textContent = rightSidebarOpen ? '⇥' : '⇤';
    // Adjust button position
    toggleRightSidebarBtn.style.right = rightSidebarOpen ? '240px' : '20px';
  });

  // Initialize button positions based on default sidebar state
  if (leftSidebar) toggleLeftSidebarBtn.style.left = '240px';
  if (rightSidebar) toggleRightSidebarBtn.style.right = '240px';


  // --- Task Switching Logic ---
  const taskLinks = document.querySelectorAll('.task-link');
  const taskControlsDivs = document.querySelectorAll('.task-controls'); // Changed selector
  const currentTaskHeader = document.getElementById('currentTask');
  
  // Set default active task (Tugas 1)
  const defaultTaskLink = document.querySelector('.task-link[data-task="task1"]');
  if (defaultTaskLink) {
      defaultTaskLink.classList.add('active');
      document.getElementById('task1Controls').style.display = 'block';
      if(currentTaskHeader) currentTaskHeader.textContent = defaultTaskLink.textContent;
  }


  taskLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      const taskId = this.getAttribute('data-task');
      
      taskLinks.forEach(lnk => lnk.classList.remove('active'));
      this.classList.add('active');
      
      taskControlsDivs.forEach(control => { // Iterate over the NodeList
        control.style.display = 'none';
      });
      const activeControls = document.getElementById(taskId + 'Controls');
      if (activeControls) {
        activeControls.style.display = 'block';
      }
      
      if(currentTaskHeader) currentTaskHeader.textContent = this.textContent;
    });
  });
  
  // --- Image Upload Logic ---
  const uploadBtn = document.getElementById('uploadBtn');
  const imageInput = document.getElementById('imageInput');
  const originalImageEl = document.getElementById('originalImage'); // Renamed for clarity
  const originalImageContainer = document.getElementById('originalImageContainer');
  const initialPrompt = document.getElementById('initialPrompt');
  const processedImageEl = document.getElementById('processedImage'); // Renamed
  const processedImageContainer = document.getElementById('processedImageContainer');
  
  if (uploadBtn) {
    uploadBtn.addEventListener('click', function() {
      if(imageInput) imageInput.click();
    });
  }
  
  if (imageInput) {
    imageInput.addEventListener('change', function() {
      if (this.files && this.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
          if(originalImageEl) originalImageEl.src = e.target.result;
          if(originalImageContainer) originalImageContainer.style.display = 'block';
          if(initialPrompt) initialPrompt.style.display = 'none';
          // Hide processed image when new image is uploaded
          if(processedImageContainer) processedImageContainer.style.display = 'none';
          if(processedImageEl) processedImageEl.src = '';
        };
        
        reader.readAsDataURL(this.files[0]);
      }
    });
  }
  
  // --- Parameter Sliders Logic ---
  const thresholdSlider = document.getElementById('thresholdValue');
  const thresholdValueDisplay = document.getElementById('thresholdValueDisplay');
  
  if (thresholdSlider && thresholdValueDisplay) {
    thresholdSlider.addEventListener('input', function() {
      thresholdValueDisplay.textContent = this.value;
    });
  }
  
  const kernelSizeSlider = document.getElementById('kernelSize');
  const kernelSizeDisplay = document.getElementById('kernelSizeDisplay');
  
  if (kernelSizeSlider && kernelSizeDisplay) {
    kernelSizeSlider.addEventListener('input', function() {
      kernelSizeDisplay.textContent = this.value;
    });
  }
  
  // --- Image Processing Logic ---
  const processButtons = document.querySelectorAll('.process-btn');
  const processedTitle = document.getElementById('processedTitle');
  
  processButtons.forEach(button => {
    button.addEventListener('click', function() {
      const method = this.getAttribute('data-method');
      
      if (!imageInput || !imageInput.files || !imageInput.files[0]) {
        alert('Silakan upload gambar terlebih dahulu');
        return;
      }
      
      const formData = new FormData();
      formData.append('image', imageInput.files[0]);
      formData.append('method', method);
      
      // Append parameters based on method
      if (method === 'threshold' && thresholdSlider) {
        formData.append('threshold_value', thresholdSlider.value);
      } else if ((method === 'erosion' || method === 'dilation') && kernelSizeSlider) {
        const kernelShapeSelect = document.getElementById('kernelShape');
        if (kernelShapeSelect) formData.append('kernel_shape', kernelShapeSelect.value);
        formData.append('kernel_size', kernelSizeSlider.value);
      }
      // No specific parameters from frontend for advanced morphology in this setup
      
      if(processedTitle) processedTitle.textContent = 'Memproses...';
      if(processedImageContainer) processedImageContainer.style.display = 'block';
      if(processedImageEl) processedImageEl.src = ''; // Clear previous image
      
      fetch('/process', {
        method: 'POST',
        body: formData
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(err => { throw new Error(err.error || 'Network response was not ok'); });
        }
        return response.json();
      })
      .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        if(processedImageEl) processedImageEl.src = 'data:image/png;base64,' + data.processed;
        if(processedTitle) processedTitle.textContent = 'Hasil: ' + button.textContent; // More descriptive title
      })
      .catch(error => {
        console.error('Error processing image:', error);
        if(processedTitle) processedTitle.textContent = 'Error: ' + error.message;
        if(processedImageEl) processedImageEl.src = ''; // Clear image on error
      });
    });
  });
});
