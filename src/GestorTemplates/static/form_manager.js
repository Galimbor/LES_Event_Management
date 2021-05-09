/**
 * Receives json data from the server, converts it to a javascript object
 * renders the UI according to that data received
 * manipulates the data (create, read, update, delete)
 * sends it back to the server
 * @param {json}   jsonForm         Django form object in json.
 * @param {json}   tiposCampo    Django campo types in json
 * @param {string}   containerDivId Id of the div where the form will be rendered
*/
var FormManager = class {

    /** CONSTRUCT OBJECT **/
    constructor(formularioJson, camposJson, tiposCampoJson, containerDivId = 'form-wrapper') {
        this.formulario = JSON.parse(formularioJson)[0];
        this.campos = JSON.parse(camposJson);
        this.tiposCampo = JSON.parse(tiposCampoJson);
        this.container = $('#' + containerDivId);
        this.activeCampo = null;

        var form = this;
        // collapse campos when clicking outside
        $(window).click(e => form.colapseCampos($('.campos-item')));
    }


    /** RENDER OBJECT **/
    /*
    * Parses json object received from the server to javascrit
    * @param {JSON} rawForm Json form data.
    * @return {object} javascript form object.
    */
    parseJsonForm(rawForm) {
        //The UI already has support for secctions 
        //in case we want to implement them
        var formObj = {
            id: 'form-1',
            title: '',
            description: '',
            campos: []
        }
        formObj.campos = JSON.parse(rawForm);
        return formObj
    }

    /* colapse html campos*/
    colapseCampos(items) {
        items.find('.card-header, .card-footer').addClass('is-hidden');
        items.find('input, textarea').not('[disabled]').addClass('is-static');
        items.removeClass('campos-item-active')
    }

    /* expand html campos*/
    expandCampos(questionItems) {
        questionItems.find('.card-header, .card-footer').removeClass('is-hidden');
        questionItems.find('input, textarea').not('[disabled]').removeClass('is-static');
        questionItems.addClass('campos-item-active')
    }

    /*
    * Shows html campo element as active and updates activeCampo variable
    * @param {JQuery Object} htmlQuestionItem
    */
    activateCampo(campo) {
        var todosCampos = $('.campos-item');
        this.colapseCampos(todosCampos);
        this.expandCampos(campo)
        form.activeCampo = form.getCampoById(campo.data('id'));
    }


    setHtmlData(obj, htmlDiv) {

        for (var key in obj.fields) {
            var value = obj.fields[key];
            var objName = obj.model.split('.')[1]
            htmlDiv.find(`.${objName}__${key}`).each(function(){
                var element = $(this);
                if (element.is(':checkbox'))
                    element.prop( "checked", value );
                else if (element.is('input'))
                    element.val(value);
                else if (key == 'position_index')
                    element.html(value + 1);
                else element.html(value);

            })
            
        }
    }

    /*
    * Obtem o template HTML do tipo de campo
    * @param {int} campoId
    */
    getCampoHtml(campoId){
        var result;
        var camposHtml = $('.campo-template')
        this.tiposCampo.forEach(
            (tipocampo, i ) => (tipocampo.pk == campoId) ? result = camposHtml.eq(i) : null
        )
        return result.clone()
    }

    setCampoEventListeners(campoHtml){
        var form = this;

        campoHtml.find('.campos-delete-btn').click(function (e) {
            form.deleteCampo($(this).data('id'));;
        })
        campoHtml.find('.campos-move-up').click(function (e) {
            e.stopPropagation();
            form.moveCampo($(this).data('id'), -1);
        })
        campoHtml.find('.campos-move-down').click(function (e) {
            e.stopPropagation();
            form.moveCampo($(this).data('id'), 1);
        })
        campoHtml.find('.campo__conteudo').change(function () {
            form.updateCampo($(this).data('id'), $(this).val());
        })
        campoHtml.find('.campo__obrigatorio').change(function () {
            var campo = form.getCampoById($(this).data('id'));
            campo.fields.obrigatorio = $(this).is(':checked');
        })
        campoHtml.click(function (e) {
            e.stopPropagation();
            form.activateCampo($(this));
        })

    }

    /*
    * Creates a html element for a campo
    * @param {object} campo
    */
    createCampoHtml(campoObj) {
        var form = this;
        //create element
        // q = HTML campo item
        var campoHtml = $('#campo-template-base').clone();
        campoHtml.removeClass('is-hidden');
        campoHtml.find('.card-content').html(
            this.getCampoHtml(campoObj.fields.tipocampoid)
        );
        //pass data id for action buttons and input fields
        campoHtml.find('a, button, input').addBack().attr(
            'data-id',
            campoObj.pk);

        //fill data
        this.setHtmlData(campoObj, campoHtml);

        if (campoObj == this.activeCampo)
            form.activateCampo(campoHtml);
        
        this.setCampoEventListeners(campoHtml);

        return campoHtml;
    }

    /*
    * Renders a campo in the form and updates its position when this parameter is passed
    * @param {string} id of the form.
    * @param {object} campo object.
    * @param {int} (optional) campo index position in the list of campos.
    */
    renderCampo(formDivId, campoObj, campoPosicao = null, focus = false) {
        //update positions
        if (campoPosicao >= 0)
            campoObj.fields.position_index = campoPosicao;

        var campoHtml = this.createCampoHtml(campoObj);
        var camposContainer = this.container.find(`#${formDivId} .campos`);
        camposContainer.append(campoHtml);
    }

    renderFormulario(){
        var formDiv = $('#form-template').clone();
        this.container.append(formDiv);
        formDiv.removeClass('is-hidden');
        formDiv.attr('id', 'form-1');
        this.setHtmlData(this.formulario, $('#gestor-templates-wrapper'))  
        var form = this; 

        //listeners 
        $('.form-header').click(function (e) {
            e.stopPropagation();
            form.expandCampos($(this));
        })
        formDiv.find('.formulario__nome').change(function (e) {
            form.formulario.fields.nome = $(this).val()
            $('.formulario__nome').html($(this).val());
        })
        $('.button.ver_form_config').click(e => $('.modal.ver_form_config').addClass('is-active'))

    }

    /*
    * Renders the entire form
    */
    renderAll() {
        //render form
        this.container.html('');
        this.renderFormulario()
        //render fields
        this.campos.forEach((q, i) => this.renderCampo('form-1', q, i));
    }

    /** MANIPULATE OBJECT **/
    /*
    * Selects a campo by id
    * @param {int} campo id/pk .
    */
    getCampoById(questionId) {
        var result;
        this.campos.some(function (q) {
            if (q.pk == questionId) {
                result = q;
                return true;
            }
        });
        return result;
    }

    /*
    * Reorders the position of campos and rerenders the form
    * @param {int} campo id/pk to be repositioned.
    */
    moveCampo(campoId, moveCount) {
        var campos = this.campos
        var campoObj = this.getCampoById(campoId);
        var oldPosition = campoObj.fields.position_index;
        var newPosition = oldPosition + moveCount;
        if (newPosition >= 0 && newPosition < campos.length) {
            //remove from old position
            campos.splice(oldPosition, 1);
            //insert at new position
            campos.splice(newPosition, 0, campoObj);
            this.renderAll();
        }
    }


    /*
    * Deletes a campo
    * @param {int} campo id/pk.
    */
    deleteCampo(campoID) {
        var campo = form.getCampoById(campoID);
        if (campo) {
            this.campos.splice(campo.fields.position_index, 1);
            this.renderAll();
        }
    }


    /*
    * Creates a campo
    * @param {int} campo type pk.
    */
    createCampo(questionType) {
        var campos = this.campos
        // TODO it should request the server to create a campo
        // this way it will always be in sync with the database
        var campoObj = {
            "model": "forms_manager.campo",
            "pk": campos.length + 100,
            "fields": {
                "conteudo": "",
                "tipocampoid": questionType,
                "text_field": "asd",
                "position_index": 1,
                "form": 6
            }
        }
        campos.push(campoObj);
        this.renderAll();
    }


    /*
    * Creates a campo
    * @param {int} campo id/pk.
    * @param {int} campo id/pk.
    */
    updateCampo(campoId, val) {
        var campo = this.getCampoById(campoId);
        campo.fields.conteudo = val;
    }

    /*
    * Posts form
    */
    saveRemotely() {
        $.ajax({
            contentType: 'application/json; charset=utf-8',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: JSON.stringify(this),
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(response) {
                console.log(response);
                //informar utilizador que nao foi possível guardar no servidor, e a respectiva razão
                //guardar localmente ?
            }
        })
    }
};