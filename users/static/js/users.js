function toggleAssociationSelect() {
    var roleSelect = document.getElementById('role_id');
    var assocDiv = document.getElementById('association-div');
    var selectedRole = roleSelect.options[roleSelect.selectedIndex]?.text?.toLowerCase();
    if (selectedRole === 'manager' || selectedRole === 'member') {
        assocDiv.style.display = 'block';
        document.getElementById('association_id').required = true;
    } else {
        assocDiv.style.display = 'none';
        document.getElementById('association_id').required = false;
    }
}
window.onload = toggleAssociationSelect;