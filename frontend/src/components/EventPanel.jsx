const EventPanel = ({ event, onDeleteClick }) => {
  return (
      <button className="relative border-4 border-black rounded m-4 shadow-xl bg-white p-8 w-4/5 max-w-4xl h-96 mx-auto"
              onClick={() => onDeleteClick(event)}>
          <h3 className="text-xl font-semibold">{event.eventName}</h3>
          <p className="text-gray-600">Date: {new Date(event.eventDate).toISOString().split('T')[0]}</p>
          <p className="mt-2">Description {event.eventDescription}</p>
          <p className="mt-2">Time: {event.eventTime}</p>
          <p className="mt-2">Location: {event.eventLocation}</p>
          <p className="mt-2">Capacity: {event.eventCapacity}</p>
          <p className="mt-2">ID: {event.id}</p>
      </button>
  )
}
export default EventPanel;


