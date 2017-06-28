import lxml.etree as et
from opimodel import actions


EXIT_SCRIPT = ('importPackage(Packages.org.csstudio.opibuilder.scriptUtil);'
               'ScriptUtil.closeAssociatedOPI(widget);')


class OpiAction(object):
    """Renderer for actions."""

    def __init__(self):
        # Dict containing any actions that require a specific method.
        self.renderers = {actions.Exit: self.render_exit}

    def render(self, widget_node, tag_name, action_list):
        actions_node = et.SubElement(widget_node, tag_name)
        for action_model in action_list:
            # Find specific method to render an action, else default to
            # simple action.
            render_method = self.renderers.get(type(action_model),
                                               self.render_simple)
            render_method(actions_node, action_model)

    def render_simple(self, actions_node, action_model):
        action_node = et.SubElement(actions_node, 'action')
        action_node.set('type', action_model._action_type)
        for key, value in vars(action_model).items():
            if not key.startswith('_'):
                n = et.SubElement(action_node, key)
                n.text = str(value)
        return action_node

    def render_exit(self, actions_node, action_model):
        """Render an exit action.

        Args:
            actions_node to be parent of the action
            action_model representing the exit action
        """
        # In CSS exit happens to use javascript.  Add properties to help with
        # rendering.
        action_model._action_type = 'EXECUTE_JAVASCRIPT'
        action_model.embedded = True
        # Render the javascript
        action_node = self.render_simple(actions_node, action_model)
        n = et.SubElement(action_node, 'scriptText')
        n.text = et.CDATA(EXIT_SCRIPT)
