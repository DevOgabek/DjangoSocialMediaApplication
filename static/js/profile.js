document.addEventListener("DOMContentLoaded", function() {
    const followForms = document.querySelectorAll('.follow-form');

    followForms.forEach(form => {
        form.addEventListener('submit', async event => {
            event.preventDefault();
            const form = event.target;
            const followButton = form.querySelector('.follow');
            const formData = new FormData(form);
            const profileId = document.querySelector('.stat').getAttribute('data-profile-pk');
            let actionUrl;

            if (followButton.textContent === 'Follow') {
                actionUrl = `/follow/${profileId}/`;
            } else if (followButton.textContent === 'Unfollow') {
                actionUrl = `/unfollow/${profileId}/`;
            }

            try {
                const response = await fetch(actionUrl, {
                    method: form.getAttribute('method'),
                    body: formData
                });
                const data = await response.json();

                if (response.ok && data.status === "success") {
                    followButton.textContent = (followButton.textContent === 'Follow') ? 'Unfollow' : 'Follow';
                    updateFollowersCount();
                } else {
                    throw new Error('Follow/unfollow operation failed.');
                }
            } catch (error) {
                console.error('AJAX request failed:', error);
            }
        });
    });

    async function updateFollowersCount() {
        try {
            const profileId = document.querySelector('.stat').getAttribute('data-profile-pk');
            const response = await fetch(`/get/followers-count/${profileId}/`);
            const data = await response.json();

            if (response.ok) {
                document.getElementById('followers').textContent = data.followers_count;
            } else {
                throw new Error('Error fetching followers count.');
            }
        } catch (error) {
            console.error('Error fetching followers count:', error);
        }
    }

    updateFollowersCount();
});
