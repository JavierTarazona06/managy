
const UserPanel = ({ user, onDeleteClick }) => {
    return (
        <div className="relative border-4 border-black rounded m-4 shadow-xl bg-white">
            <button
                onClick={() => onDeleteClick(user)}
                className="border bg-red-500 rounded-3xl absolute top-2 px-4 right-2 text-white font-bold hover:bg-red-600 shadow-xl"
            >
                Delete
            </button>
            <h1 className="font-bold p-1">
                {user.first_name}
            </h1>
            <p className="p-1">User Role: {user.role}</p>
            <p className="p-1">User Email: {user.email} </p>
            <p className="p-1">User ID: {user.id}</p>
            <p className="p-1">User username: {user.username}</p>
            <p className="p-1">User Recreational Venue ID: {user.recreational_venue}</p>
        </div>
    )
}
export default UserPanel;

